

//before run/submit

var beforeSubmit = function(){
  document.querySelector('#sub').style.display = 'inline';
  document.querySelector('#runbot').disabled = true;
  document.querySelector('#runbot').style.cursor = "not-allowed";
  document.querySelector('#subbot').disabled = true;
  document.querySelector('#subbot').style.cursor = "not-allowed";
}
var afterSubmit = function(){
  document.querySelector('#sub').style.display = 'none';
  document.querySelector('#runbot').disabled = false;
  document.querySelector('#runbot').style.cursor = "auto";
  document.querySelector('#subbot').disabled = false;
  document.querySelector('#subbot').style.cursor = "auto ";
}
// upon run
var run = function(data,accepted){
  console.log(data.status);
  if(data.status.description!="Processing"){
    accepted = true;
    if(data.status.description!="Accepted"){
    document.querySelector('#out').innerHTML = data.status.description+'\n';
      if(data.stderr)
        document.querySelector('#out').innerHTML+=atob(data.stderr);
    
        }
    if(data.status.description=="Accepted"){
         document.querySelector('#out').innerHTML+=atob(data.stdout);
    }

    

  }
  afterSubmit();
  return accepted;
  }
var submit = function(data,accepted){
  console.log(data.status);
  if(data.status.description!="Processing"){
    accepted = true;
    if(data.status.description!="Accepted"){
      document.querySelector('#out').innerHTML = data.status.description+'\n';
        if(data.stderr)
          document.querySelector('#out').innerHTML+=atob(data.stderr);
      
          }
      if(data.status.description=="Accepted"){
           var expected = document.querySelector('#customoutput').innerHTML;
           var actual = atob(data.stdout);
           console.log(expected)
           console.log(actual)
           if(expected==actual)
              {
                if(!solved[cur_question]){
                   total+=scores[cur_question];
                   document.querySelector('#score').innerHTML = con_two(total);
                   let question = 'q'+(cur_question+1).toString()+'s';
                   document.querySelector('#'+question).value= "true";
                   solved[cur_question] = true;
                }
              }     
      }
  
      
  }
  afterSubmit();
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


var scores = [15,35,50]
var solved = [false,false,false]
var total = 0;
document.querySelector('#q1s').value= "false";
document.querySelector('#q2s').value = "false";
document.querySelector('#q3s').value = "false";
document.querySelector('#q1').value = qs[0];
document.querySelector('#q2').value = qs[1];
document.querySelector('#q3').value = qs[2];

var inputs = []
var outputs = []
var ins = document.querySelectorAll('#inputs li')
var outs = document.querySelectorAll('#outputs li')
Array.from(ins).forEach((e)=>{
  let input = e.innerHTML;
  inputs.push(input);
})
Array.from(outs).forEach((e)=>{
  let output = e.innerHTML;
  outputs.push(output);
})



var codes = ["","",""];
var cur_question = 0;

var loadcontent = (i)=>{
  document.querySelector('.title').innerHTML = titles[i];
  document.querySelector('.content').innerHTML = contents[i];
  editor.setValue(codes[i]);
  document.querySelector('#inp').innerHTML = "";
  document.querySelector('#out').innerHTML = "";
  document.querySelector('#hiddeninp').innerHTML = inputs[i];
  document.querySelector('#customoutput').innerHTML = outputs[i];
  console.log(inputs[i],outputs[i]);
  return i;
} 
// initialize
loadcontent(cur_question);
document.querySelector('#score').innerHTML = con_two(total);



var questionlist = document.querySelector('#questions');
questionlist.addEventListener('click',(e)=>{
  codes[cur_question] = editor.getValue();
  
  var i = Array.from(e.target.parentNode.children).indexOf(e.target);
  cur_question = loadcontent(i);
  
  // console.log(i);
})


//run button event
document.querySelector('#sub').style.display = "none";
document.querySelector('#runbot').addEventListener('click',(e)=>{
  e.preventDefault();
    
    
  
  
    language = lid[langselect.value];
    sourcecode = editor.getValue();
    inputcode  = document.querySelector('#inp').value;
    beforeSubmit();
    runCode(run);
    // afterSubmit();
});


//submit event
document.querySelector('#subbot').addEventListener('click',(e)=>{
  e.preventDefault();
    
    
  

    language = lid[langselect.value];
    sourcecode = editor.getValue();
    inputcode  = document.querySelector('#hiddeninp').value;
    beforeSubmit();
    runCode(submit);
    // afterSubmit();
    
});






//timer
var i = 0
var hour = 1;
var min = 29;
var sec = 59;
function con_two(n){
   if(n/10>=1)
     return n.toString();
  else
     return "0"+n.toString();
}
document.querySelector('#timer').innerHTML = "0"+ hour.toString()+":"+ con_two(min)+":"+con_two(sec);

var timer  = setInterval(
  ()=>{
     
     sec--;
   
     if(sec==-1 && min>=0)
       {
         min--;
         sec = 59;
       } 
     if(min==-1 && hour>=0)
     {
       hour--;
       min = 59;
     }
     if(hour==-1){

       document.querySelector('#finish').submit();
       clearInterval(timer);
     }
   if(hour!=-1)
   document.querySelector('#timer').innerHTML = "0"+ hour.toString()+":"+ con_two(min)+":"+con_two(sec);
       
  },
  1000
)
document.addEventListener('contextmenu',(e)=>{
  e.preventDefault();
})

