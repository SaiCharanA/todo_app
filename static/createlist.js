$(document).ready(function(){
	$('button').click(function(){
		var task_id = $(this).attr('id');
		var current_task = $('p'+'#'+task_id+'.taskname').text();
		var btn_typ = $(this).attr('class');		
		if (btn_typ == 'edittask'){
				var updated_task = prompt("Update the task");
				if (updated_task === null){
					return;
				}
				else{
					$('p'+'#'+task_id+'.taskname').text(updated_task);
					$.ajax({
						url : "/updatetask",
						type : "POST",
						data : {taskid:task_id,updatedtask:updated_task},
					});
					return;	
				}
		}
		else if (btn_typ == 'deletetask'){
				$('div'+'#'+task_id+'.listblock').remove();
				$('ul'+'.deleteblock').append("<li style='font-size:15px'>"+current_task+"</li>");
				$.ajax({
					url : "/removetask",
					type : "POST",
					data : {taskid:task_id},
				});
		return;
		}
		else if (btn_typ == 'completetask'){
				$('div'+'#'+task_id+'.listblock').remove();
				$('ul'+'.completeblock').append("<li style='font-size:15px'>"+current_task+"</li>");
				$.ajax({
					url : "/finishtask",
					type : "POST",
					data : {taskid:task_id},
				});
		return;
		}
	})
return;
})
