
//language_ids 
var lid = {
    'text/x-csrc': 49,
    'text/x-c++src':54,
    'text/x-java': 62,
    'python': 71,
     'javascript': 63
  }

var language,sourcecode,inputcode;
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

var uploaded;
document.querySelector('#inputfile').addEventListener('change',(e)=>{
   
    uploaded = false;
    var file_reader = new FileReader()
    
    file_reader.onload = function(e){
       
        inputcode = e.target.result;
        uploaded = true;
    }

    
        
       file_reader.readAsText(e.target.files[0])
    //    console.log(input);
    }
);
document.querySelector('#test').addEventListener('click',(e)=>{
    e.preventDefault();
    document.querySelector("#failure").style.display = "none";
    document.querySelector("#success").style.display = "none";
    
if(uploaded){
    language = lid[langselect.value];
    sourcecode = editor.getValue();
    document.querySelector('#process').style.display = "inline";
    fetch("https://judge0-ce.p.rapidapi.com/submissions", {
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
          fetch("https://judge0-ce.p.rapidapi.com/submissions/"+token+"?base64_encoded=true", {
        "method": "GET",
        "headers": {
          "x-rapidapi-key": "c62c0db617msh7a7282a1a7c80d3p1a88d3jsn7b1f12f9ed62",
          "x-rapidapi-host": "judge0.p.rapidapi.com"
        }
      })
      .then(response => {
        //process result
        response.json().then(data=>{
            
        if(data.status.description!="Processing"){
          document.querySelector('#process').style.display = "none";
          
           accepted = true;
           if(data.status.description!="Accepted"){
           document.querySelector("#failure").style.display = "inline";

            // console.log(data.stderr);
           }
           else{
            document.querySelector('#success').style.display = "inline";
            document.querySelector('#output').value = atob(data.stdout);
            console.log(document.querySelector('#output').value);
            // console.log(data.stdout);
           }
        //    document.querySelector('#sub').style.display = 'none';
        }
        
        })
    })
    .catch(err => {
        console.error(err);
    });
          },3000)
    
       })
    })
    .catch(err => {
        console.error(err);
    });
}
else{
    document.querySelector("#uperr").style.display = "inline";
}
});

//UI


document.querySelector('')