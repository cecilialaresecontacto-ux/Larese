import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
U="/root/.claude/uploads/17f013b8-a35a-5b09-871c-8efeeb67d8b3/"
items={"paradoxe":(U+"172f803c-image.webp",28),"divine":(U+"578f81ff-image.jpg",22),
       "valentino":(U+"d2c45705-image.jpg",22),"missdior":(U+"9a040d32-image.jpg",18),"delina":(U+"eda3bdee-image.jpg",14)}
for name,(p,th) in items.items():
    im=Image.open(p).convert("RGB"); w,h=im.size
    work=im.copy()
    S=(255,0,255)
    step=max(1,w//60)
    seeds=[(x,0) for x in range(0,w,step)]+[(x,h-1) for x in range(0,w,step)]+[(0,y) for y in range(0,h,step)]+[(w-1,y) for y in range(0,h,step)]
    for s in seeds:
        if work.getpixel(s)!=S: ImageDraw.floodfill(work,s,S,thresh=th)
    a=np.asarray(work); m=~((a[...,0]==255)&(a[...,1]==0)&(a[...,2]==255))
    if name=="delina": m[:int(h*0.08),:int(w*0.15)]=False
    if name=="paradoxe":
        z=Image.new("L",(w,h),0); ImageDraw.Draw(z).polygon([(300,1600),(1000,1592),(1260,1585),(1405,1542),(1458,1490),(1466,1420),(2000,1420),(2000,2000),(300,2000)],fill=255)
        m&=~(np.asarray(z)>0)
    mask=Image.fromarray((m*255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1))
    out=im.copy(); out.putalpha(mask); bb=mask.point(lambda v:255 if v>40 else 0).getbbox()
    out.crop(bb).save(f"cut/{name}.png"); print(name,bb)
