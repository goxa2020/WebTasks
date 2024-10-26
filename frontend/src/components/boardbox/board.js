import React, { useState } from 'react';
import Column from './column.js';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';
import styles from './style.module.css'
import Popup from '../popup/popup.js';

const initialData = {
  "todo": [
    { id: '1', title: 'Задача 1', assignee: 'Федор' },
    { id: '2', title: 'Задача 2', assignee: 'Шарик' },
  ],
  "inProgress": [
    { id: '3', title: 'Задача 3', assignee: 'Эльдар' },
  ],
  "done": [
    { id: '4', title: 'Задача 4', assignee: 'Джарахов' },
  ],
};

const Board = ({ title }) => {
  const [isPopupVisible, setIsPopupVisible] = useState(false);

  const handleOpenPopup = () => {
    setIsPopupVisible(true);
  };

  const handleClosePopup = () => {
    setIsPopupVisible(false);
  };
  const [tasks, setTasks] = useState(initialData);

  const onDragEnd = (result) => {
    if (!result.destination) return;

    const { source, destination } = result;
    console.log(source)
    console.log(destination)
    if (source.droppableId !== destination.droppableId) {
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
      <div className={styles.board}>
        <Column title="Беклог" tasks={tasks.todo} droppableId={'todo'}/>
        <Column title="В процессе" tasks={tasks.inProgress} droppableId={'inProgress'}/>
        <Column title="Выполнено" tasks={tasks.done} droppableId={'done'}/>
      </div>
      <div>
      <h1>Пример всплывающего окна</h1>
      <button onClick={handleOpenPopup}>Показать всплывающее окно</button>
      {isPopupVisible && (
        <div className={styles.popup}>
        <div className={styles.popupContent}>
          <h2>{title}</h2>
          <p>Пароли должны совпадать.</p>
          <button onClick={handleClosePopup}>ОК</button>
        </div>
      </div>
      )}
    </div>
    </DragDropContext>
  );
};

export default Board;
