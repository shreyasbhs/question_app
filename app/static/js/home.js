
var createQuestionList = 
(
()=>{
var questionListBefore = Array.from(document.querySelectorAll('.question-list-before li'));
var questionListAfter = document.querySelector('.question-list-after');
console.log(questionListBefore)
var i = 0;
var pno = 0;
while(i<questionListBefore.length){
    pno+=1;
    var page = document.createElement('ul')
    page.classList.add('question-page');
    
    for(var j = i;j<i+3&&j<questionListBefore.length;j++)
       {
           var li = questionListBefore[j];
           console.log(li)
           page.appendChild(li)
           

       }
   
    page.style.display = "none"
    console.log(page)
    i+=3;
    questionListAfter.appendChild(page);
 
    

}
var pages = Array.from(document.querySelectorAll('.question-page'))
var pageNo = document.querySelector('#page-no')
pageNo.innerHTML = "1";
pages[0].style.display = 'block';
document.querySelector('#next-page').addEventListener('click', ()=>{
    let i = parseInt(pageNo.innerHTML)
    if(i<pno){
    pages[i-1].style.display = 'none'
    pageNo.innerHTML = (i+1).toString();
    pages[i].style.display = 'block';
    }

})
document.querySelector('#pre-page').addEventListener('click', ()=>{
    let i = parseInt(pageNo.innerHTML)
    if(i>1){
    pages[i-1].style.display = 'none'
    pageNo.innerHTML = (i-1).toString();
    // if(i-2>0)
    pages[i-2].style.display = 'block';
    }
})
})();


