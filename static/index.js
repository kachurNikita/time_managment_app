//  get all buttons with class 'btn_task'
let btns = document.querySelectorAll('.btn_task');

// get div with class 'tasks' in order to append child in to
let tasks_block = document.querySelector('.tasks');

// Create tag when task breakdown content
let task_breakdown = document.createElement('div');

// on click catch btn, add content to  created clock and append it to html
for (let i = 0; i < btns.length; i++) {
    task_breakdown.textContent = ''
    btns[i].addEventListener('click', function(e) {
    task_breakdown.textContent = e.target.value
    tasks_block.append(task_breakdown)
   })
}

