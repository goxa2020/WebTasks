import React from 'react';
import { Droppable, Draggable } from 'react-beautiful-dnd';
import TaskCard from './taskcard.js';


const Column = ({ title, tasks }) => {
  return (
    <Droppable droppableId={title.toLowerCase().replace(' ', '-')}>
      {(provided) => (
        <div className="column" ref={provided.innerRef} {...provided.droppableProps}>
          <h2>{title}</h2>
          {tasks.map((task, index) => (
            <Draggable key={task.id} draggableId={task.id} index={index}>
              {(provided) => (
                <div ref={provided.innerRef} {...provided.draggableProps} {...provided.dragHandleProps}>
                  <TaskCard task={task} />
                </div>
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
