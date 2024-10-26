import React from 'react';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';
import styles from './style.module.css'

const TaskCard = ({ task, provided }) => {
  return (
    <div onClick={() => alert(`Edit ${task.title}`)} className={styles.taskCard} ref={provided.innerRef} {...provided.draggableProps} {...provided.dragHandleProps}>
      <h3>{task.title}</h3>
      <p>Исполнитель: {task.assignee}</p>
      <button className={styles.btn} onClick={() => alert(`Delete ${task.title}`)}>Удалить <i class="fa fa-trash" aria-hidden="true"></i></button>
    </div>
  );
};
export default TaskCard;
