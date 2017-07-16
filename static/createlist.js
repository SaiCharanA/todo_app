$(document).ready(function(){
	$('button').click(function(){
		var task_id = $(this).attr('id');
		var btn_typ = $(this).attr('class');		
		if (btn_typ == 'edittask'){
				var updated_task = prompt("Update the task");
				$('p'+'#'+task_id+'.taskname').text(updated_task);
				$.ajax({
					url : "/updatetask",
					type : "POST",
					data : {taskid:task_id,updatedtask:updated_task},
				});	

		}
		else if (btn_typ == 'deletetask'){
				$('div'+'#'+task_id+'.taskblock').remove();
				$.ajax({
					url : "/removetask",
					type : "POST",
					data : {taskid:task_id},
				});
				
		}
	})
})
