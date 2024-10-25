import React from 'react';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';

const TaskCard = ({ task }) => {
  return (
    <div className="task-card">
      <h3>{task.title}</h3>
      <p>Assignee: {task.assignee}</p>
      <button onClick={() => alert(`Edit ${task.title}`)}>Edit</button>
      <button onClick={() => alert(`Delete ${task.title}`)}>Delete</button>
    </div>
  );
};

export default TaskCard;
