
// upon run
var run = function(data,accepted){
  console.log(data.status);
  if(data.status.description!="Processing"){
    accepted = true;
    document.querySelector('#sub').style.display = 'none';
    if(data.stderr)
     document.querySelector('#out').innerHTML = data.stderr;
    else{
    
      var custom = document.querySelector('#customoutput').innerHTML;
      console.log("run sucessfully");
         }
  }
  return accepted;
  }
var submit = function(data,accepted){
  console.log(data.status);
  if(data.status && data.status.description!="Processing"){
    accepted = true;
    document.querySelector('#sub').style.display = 'none';
    if(data.stderr)
     document.querySelector('#out').innerHTML = atob(data.stderr);
    else{
    
      var custom = document.querySelector('#customoutput').innerHTML;
      console.log(data.stdout);
      document.querySelector('#out').innerHTML = atob(data.stdout);
      console.log("accepted");
      // document.querySelector('form').submit();

         }
  }
  return accepted;
}


var runCode = (process)=>{
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
        var accepted = false;
  
        var feed = setInterval(()=>{
        if(accepted){
         clearInterval(feed);
         return;
        }
  console.log(data.status);
        fetch("https://judge0.p.rapidapi.com/submissions/"+token+"?base64_encoded=true", {
      "method": "GET",
      "headers": {
        "x-rapidapi-key": "c62c0db617msh7a7282a1a7c80d3p1a88d3jsn7b1f12f9ed62",
        "x-rapidapi-host": "judge0.p.rapidapi.com"
      }
    })
    .then(response => {
      //process result
      response.json().then(data=>{
       accepted = process(data,accepted);
      
       
      })
  }).catch(err => {
    console.error(err);
  });
},3000)})
}).catch(err => { console.error(err);
});
};




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
var solved = false;

//run button event
document.querySelector('#sub').style.display = "none";
document.querySelector('#runbot').addEventListener('click',(e)=>{
  e.preventDefault();
    
    

    language = lid[langselect.value];
    sourcecode = editor.getValue();
    inputcode  = document.querySelector('#inp').value;
    runCode(run);
});


//submit event
document.querySelector('#subbot').addEventListener('click',(e)=>{
  e.preventDefault();
    
    

    language = lid[langselect.value];
    sourcecode = editor.getValue();
    inputcode  = document.querySelector('#hiddeninp').value;
    runCode(submit);
    
});



