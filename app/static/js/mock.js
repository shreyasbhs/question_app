
//setting margin of code mirror
var codemirror = document.querySelectorAll('.CodeMirror');
codemirror.forEach((c)=>{
  c.style.marginRight = "10px";
})
var language;

//language_ids 
var lid = {
  'text/x-csrc': 49,
  'text/x-c++src':54,
  'text/x-java': 62,
  'python': 71,
   'javascript': 63
}



document.querySelector('#content').innerHTML = contents[0];
//initial settings for code mirror
var editor = CodeMirror.fromTextArea(document.querySelector('#code'),{
  lineNumbers:true,
  mode: document.querySelector('#lang').value,
  theme: document.querySelector('#theme').value
});
langselect = document.querySelector('#lang');
langselect.addEventListener('change',()=>{
  mode = langselect.value;
  editor.setOption("mode",mode)
})
themeselect = document.querySelector('#theme')
themeselect.addEventListener('change',()=>{
  theme = themeselect.value;
  editor.setOption("theme",theme);
})


var sourcecode,inputcode;


//run button event
document.querySelector('#sub').style.display = "none";
document.querySelector('#subbot').addEventListener('click',(e)=>{
  e.preventDefault();
 
          document.querySelector('#sub').style.display = "inline";
    

    language = lid[langselect.value];
    sourcecode = editor.getValue();
    inputcode  = document.querySelector('#inp').value;
fetch("https://judge0.p.rapidapi.com/submissions", {
	"method": "POST",
	"headers": {
		"Content-Type": "application/json",
		"x-rapidapi-key": "c62c0db617msh7a7282a1a7c80d3p1a88d3jsn7b1f12f9ed62",
		"x-rapidapi-host": "judge0.p.rapidapi.com"
  },
  'Access-Control-Allow-Origin':'*',
	"body":JSON.stringify( {
		"language_id":language,
		"source_code": sourcecode,
		"stdin": inputcode
	})
})
.then(response => {
      response.json().then(data=>{
      console.log(data);
      let token = data.token;
      fetch("https://judge0.p.rapidapi.com/submissions/"+token, {
    "method": "GET",
    "headers": {
      "x-rapidapi-key": "c62c0db617msh7a7282a1a7c80d3p1a88d3jsn7b1f12f9ed62",
      "x-rapidapi-host": "judge0.p.rapidapi.com"
    }
  })
  .then(response => {
    //process result
    response.json().then(data=>{
      if(data.stderr)
        document.querySelector('#out').innerHTML  = data.stderr;
      else
        document.querySelector('#out').innerHTML = data.stdout;
      document.querySelector('#sub').style.display = "none";
    
    })
})
.catch(err => {
	console.error(err);
});

   })
})
.catch(err => {
	console.error(err);
});
}) 

