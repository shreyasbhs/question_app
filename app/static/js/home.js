//initial list of questions

var questionListBefore = Array.from(document.querySelectorAll('.question-list-before li'));
var questionListAfter = document.querySelector('.question-list-after');
var totalPages;


var createQuestionList = 

(list)=>{
questionListAfter.innerHTML = "";
// console.log(questionListBefore)
var index = 0;
totalPages= 0;
while(index<list.length){
    totalPages+=1;
    var page = document.createElement('ul')
    
    page.classList.add('question-page');
    let head = document.createElement('li');
    head.setAttribute('id','qlist-title')
    head.innerHTML = '<span class = "slno">#</span> <span class = "title" style = "text-align:center">title</span>'
    head.innerHTML+= '<span class="difficulty" style = "text-align:center">Difficulty</span><span class = "solution">Sol</span>';
    page.appendChild(head);
    for(var j = index;j<index+3&&j<list.length;j++)
       {
           var li = list[j];
        //    console.log(li)
           page.appendChild(li)
           

       }
   
    page.style.display = "none"
    console.log(page)
    index+=3;
    questionListAfter.appendChild(page);
 
    

}
var pages = Array.from(document.querySelectorAll('.question-page'))


pages[0].style.display = 'block';
var nextp =  ()=>{
    document.querySelector('#next-page').style.display = 'block';
    document.querySelector('#pre-page').style.display = 'block';
    var pageNo = document.querySelector('#page-no')
    let i = parseInt(pageNo.innerHTML)-1;
    if(i+1<totalPages){
    console.log(i)
    if(i+1==totalPages-1)
       document.querySelector('#next-page').style.display = 'none';
    
    pages[i].style.display = 'none'
    
    pages[i+1].style.display = 'block';
    pageNo.innerHTML = (i+2).toString();
    }

};
var prev = ()=>{
    document.querySelector('#next-page').style.display = 'block';
    document.querySelector('#pre-page').style.display = 'block';
    var pageNo = document.querySelector('#page-no')
    let i = parseInt(pageNo.innerHTML)-1;
    if(i-1>=0){
        // console.log(i);
    if(i-1==0)
    document.querySelector('#pre-page').style.display = 'none';
      
    pages[i].style.display = 'none'
    pageNo.innerHTML = (i).toString();
    // if(i-2>0)
    pages[i-1].style.display = 'block';
    }
}
document.querySelector('#pre-page').remove();
document.querySelector('#next-page').remove();
document.querySelector('#page-no').remove();
var navigate = document.querySelector('.page-navigate');
var pre = document.createElement('span');
var next = document.createElement('span');
var page = document.createElement('span')
page.innerHTML = "1";
pre.setAttribute('id','pre-page');
next.setAttribute('id','next-page');
page.setAttribute('id','page-no');
pre.innerHTML = '<';
next.innerHTML = '>';
pre.style.display = 'none';
navigate.appendChild(next);
navigate.appendChild(page);
navigate.appendChild(pre);

var preButton = document.querySelector('#pre-page'); 
var nextButton = document.querySelector('#next-page');
preButton.addEventListener('click',prev);
nextButton.addEventListener('click',nextp);

};


createQuestionList(questionListBefore);


//search question by name
var questionSearch = document.querySelector('#question-search')
questionSearch.addEventListener('input',()=>{
    var enteredString = questionSearch.value;
     var questions = []
     questionListBefore.forEach((question)=>{
         if(enteredString === "")
            questions.push(question);
        else if((question.innerHTML.toLowerCase()).indexOf(enteredString.toLowerCase())!=-1)
            questions.push(question);     
     });
     createQuestionList(questions);
    })
$('question-page').slideDown();
// /
//     e.preventDefault();
// })