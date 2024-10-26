import React from 'react';
import { Droppable, Draggable } from 'react-beautiful-dnd';
import TaskCard from './taskcard.js';
import styles from './style.module.css'

const Column = ({ title, tasks, droppableId }) => {
  return (
    <Droppable droppableId={droppableId}>
      {(provided) => (
        <div className={styles.column} ref={provided.innerRef} {...provided.droppableProps}>
          <h2>{title}</h2>
          {tasks.map((task, index) => (
            <Draggable key={task.id} draggableId={task.id} index={index}>
              {(provided) => (
                <TaskCard task={task} provided={provided} />
              )}
            </Draggable>
          ))}
          {provided.placeholder}
          <button className={styles.btnadd}><i class="fa fa-plus" aria-hidden="true"></i> Добавить задачу</button>
        </div>
      )}
    </Droppable>
  );
};

export default Column;
