import React from 'react';
import { Droppable, Draggable } from 'react-beautiful-dnd';
import TaskCard from './taskcard.js';
import styles from './style.module.css'

const Column = ({ tasks, droppableId, popupSetters }) => {
  return (
    <Droppable droppableId={droppableId}>
      {(provided) => (
        <div className={styles.column} ref={provided.innerRef} {...provided.droppableProps}>
          {tasks && tasks.map((task, index) => (
            <Draggable key={task.id} draggableId={task.id.toString()} index={index}>
              {(provided) => (
                task && <TaskCard task={task} provided={provided} popupSetters={popupSetters}/>
              )}
            </Draggable>
          ))}
          {provided.placeholder}
          <button className={styles.btnadd}><i className={"fa fa-plus"} aria-hidden="true"></i> Добавить задачу</button>
        </div>
      )}
    </Droppable>
  );
};

export default Column;
