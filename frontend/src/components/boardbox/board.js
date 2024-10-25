import React, { useState } from 'react';
import Column from './column.js';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';

const initialData = {
  todo: [
    { id: '1', title: 'Task 1', assignee: 'Alice' },
    { id: '2', title: 'Task 2', assignee: 'Bob' },
  ],
  inProgress: [
    { id: '3', title: 'Task 3', assignee: 'Charlie' },
  ],
  done: [
    { id: '4', title: 'Task 4', assignee: 'David' },
  ],
};

const Board = () => {
  const [tasks, setTasks] = useState(initialData);

  const onDragEnd = (result) => {
    if (!result.destination) return;

    const { source, destination } = result;

    if (source.droppableId === destination.droppableId) {
      const columnTasks = Array.from(tasks[source.droppableId]);
      const [movedTask] = columnTasks.splice(source.index, 1);
      columnTasks.splice(destination.index, 0, movedTask);

      setTasks((prevTasks) => ({
        ...prevTasks,
        [source.droppableId]: columnTasks,
      }));
    } else {
      const sourceTasks = Array.from(tasks[source.droppableId]);
      const destinationTasks = Array.from(tasks[destination.droppableId]);
      const [movedTask] = sourceTasks.splice(source.index, 1);

      destinationTasks.splice(destination.index, 0, movedTask);

      setTasks((prevTasks) => ({
        ...prevTasks,
        [source.droppableId]: sourceTasks,
        [destination.droppableId]: destinationTasks,
      }));
    }
  };

  return (
    <DragDropContext onDragEnd={onDragEnd}>
      <Droppable droppableId="board" direction="horizontal">
        {(provided) => (
          <div className="board" ref={provided.innerRef} {...provided.droppableProps}>
            <Column title="To Do" tasks={tasks.todo} />
            <Column title="In Progress" tasks={tasks.inProgress} />
            <Column title="Done" tasks={tasks.done} />
            {provided.placeholder}
          </div>
        )}
      </Droppable>
    </DragDropContext>
  );
};

export default Board;
