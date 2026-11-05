"""Extract actual representative pixels and render a deterministic color-data chart."""
from pathlib import Path
import argparse,json,hashlib,math,colorsys
import numpy as np
from PIL import Image,ImageOps,ImageDraw,ImageFont

def extract(path,count=12,crop=None,points=None):
    decoded=ImageOps.exif_transpose(Image.open(path));source=decoded.convert('RGB');w,h=source.size
    box=crop or [0,0,w,h]
    if not(0<=box[0]<box[2]<=w and 0<=box[1]<box[3]<=h):raise ValueError('Invalid crop')
    if 'A' in decoded.getbands() and decoded.getchannel('A').crop(box).getextrema()[0]<255:raise ValueError('Crop to opaque content first; transparent pixels must not enter this palette')
    image=source.crop(box);small=image.copy();small.thumbnail((512,512))
    q=small.quantize(colors=min(64,count*4),method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
    table=q.getpalette();clusters=sorted(q.getcolors(),reverse=True)
    candidates=[(np.array(table[i*3:i*3+3],dtype=float),n) for n,i in clusters]
    # Greedy distinct representatives, weighted mildly by actual cluster size.
    chosen=[]
    while candidates and len(chosen)<count:
        if not chosen:index=0
        else:index=max(range(len(candidates)),key=lambda i:min(np.linalg.norm(candidates[i][0]-c) for c in chosen)*(candidates[i][1]/small.width/small.height)**.2)
        color,n=candidates.pop(index)
        if chosen and min(np.linalg.norm(color-c) for c in chosen)<5:continue
        chosen.append(color)
    pixels=np.array(source); step=max(1,int(math.sqrt(image.width*image.height/300000)))
    grid=pixels[box[1]:box[3]:step,box[0]:box[2]:step];flat=grid.reshape(-1,3).astype(float)
    swatches=[];seen=set()
    def add(x,y):
        if not(box[0]<=x<box[2] and box[1]<=y<box[3]):raise ValueError('Point outside content crop')
        rgb=pixels[y,x].tolist();key=tuple(rgb)
        if key in seen:return
        seen.add(key);swatches.append(dict(rgb=rgb,hex='#'+''.join(f'{v:02X}' for v in rgb),source_point=[x,y]))
    for x,y in points or []:add(x,y)
    for c in chosen:
        if len(swatches)>=count:break
        k=int(np.argmin(np.sum((flat-c)**2,axis=1)));gy,gx=divmod(k,grid.shape[1]);add(box[0]+gx*step,box[1]+gy*step)
    # Retain hue families, each from dark to light, rather than imply area order.
    swatches.sort(key=lambda s:(round(colorsys.rgb_to_hsv(*[v/255 for v in s['rgb']])[0]*6),sum(s['rgb'])))
    return source,dict(source=str(Path(path).resolve()),source_sha256=hashlib.sha256(Path(path).read_bytes()).hexdigest(),size=[w,h],crop=box,method='Pillow median-cut candidate clusters; RGB-distance/population representative selection; snap to actual source pixels; optional explicit point priority',profile='RGB values as decoded; sRGB interpretation assumed, no automatic creative grade',count=len(swatches),requested_count=count,equal_width_not_area=True,swatches=swatches)

def render(data,out):
    out=Path(out)
    if (out/'color-card.png').exists() or (out/'palette.json').exists():raise FileExistsError('Choose a new version directory')
    out.mkdir(parents=True,exist_ok=True)
    im=Image.new('RGB',(1920,1080),'white');d=ImageDraw.Draw(im)
    font_path=Path('C:/Windows/Fonts/arial.ttf')
    if not font_path.exists():raise FileNotFoundError('Pass a local Arial-compatible font by adapting the explicit font configuration')
    font=ImageFont.truetype(str(font_path),36)
    n=len(data['swatches']);cols=min(6,n);rows=math.ceil(n/cols);margin,gap=18,15;cw=(1920-2*margin-(cols-1)*gap)//cols;rh=(1080-2*margin-(rows-1)*18)//rows;checks=[]
    for i,s in enumerate(data['swatches']):
        row,col=divmod(i,cols);x=margin+col*(cw+gap);y=margin+row*(rh+18);bh=rh-65
        d.rectangle([x,y,x+cw-1,y+bh-1],fill=tuple(s['rgb']))
        bbox=d.textbbox((0,0),s['hex'],font=font);tw=bbox[2]-bbox[0]
        d.text((x+(cw-tw)/2,y+bh+11-bbox[1]),s['hex'],font=font,fill='black')
        center=[x+cw//2,y+bh//2];assert im.getpixel(tuple(center))==tuple(s['rgb']);checks.append(dict(hex=s['hex'],center=center,passed=True))
    im.save(out/'color-card.png');data['render_checks']=checks
    (out/'palette.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    return out/'color-card.png'

def main():
    p=argparse.ArgumentParser();p.add_argument('--image',required=True);p.add_argument('--out',required=True);p.add_argument('--count',type=int,default=12);p.add_argument('--crop');p.add_argument('--points');a=p.parse_args()
    if not 1<=a.count<=12:raise ValueError('This grid supports 1..12 actual colors')
    crop=list(map(int,a.crop.split(','))) if a.crop else None
    points=[tuple(map(int,x.split(','))) for x in a.points.split(';')] if a.points else []
    source,data=extract(a.image,a.count,crop,points)
    for s in data['swatches']:assert list(source.getpixel(tuple(s['source_point'])))==s['rgb']
    print(render(data,a.out))
if __name__=='__main__':main()
