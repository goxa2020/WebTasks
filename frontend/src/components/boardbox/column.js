import React from 'react';
import { Droppable, Draggable } from 'react-beautiful-dnd';
import TaskCard from './taskcard.js';
import styles from './style.module.css'

const Column = ({ title, tasks }) => {
  return (
    <Droppable droppableId={title.toLowerCase().replace(' ', '-')}>
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
        </div>
      )}
    </Droppable>
  );
};

export default Column;
