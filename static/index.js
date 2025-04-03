
let content_block = document.querySelector('.content_block')
//  get all buttons with class 'btn_task'
let btns = document.querySelectorAll('.btn_task');

// get div with class 'tasks' in order to append child in to
let tasks_block = document.querySelector('.tasks');

// delete button
let delete_btn = document.createElement('button')
let task_breakdown_content = document.createElement('div')
delete_btn.textContent = 'DELETE TASK'


function show_task_breakdown(){
    for (let i = 0; i < btns.length; i++) {
        last_clicked_button = null
        btns[i].addEventListener('click', function(e) {
            current_clicked_button = e.target.value
            quadrat_name = e.target.name
            if (current_clicked_button === last_clicked_button) {
                content_block.textContent = ''
                last_clicked_button = null
                tasks_block.removeChild(delete_btn)
            }
            else {
                content_block.textContent = btns[i].dataset.value
                last_clicked_button = e.target.value
                delete_btn.value = quadrat_name
                delete_btn.dataset.tag = btns[i].textContent
                tasks_block.append(delete_btn)
            }
       })
    }
}


function delete_task() {
    delete_btn.addEventListener('click', function (e) {
        value = e.target.dataset.tag
        quadrat_name = e.target.value
        fetch('/delete_task', {
            // Declare what type of data we're sending
            headers: {
                'Content-Type': 'application/json'
            },
            // Specify the method
            method: 'POST',
            // A JSON payload
            body: JSON.stringify({quadrat_name, value})
        }).then(() => {
            window.location.reload()
        })
})
}

show_task_breakdown()

delete_task()