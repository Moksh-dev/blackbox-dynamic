document.addEventListener(
"mousemove",

e=>{

document.querySelectorAll(
".orb"

)

.forEach(

(el,index)=>{

el.style.transform=

`translate(

${e.clientX/
((index+1)*60)}px,

${e.clientY/
((index+1)*60)}px

)`

})

})