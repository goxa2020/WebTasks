import React, { useEffect, useState } from 'react';
import Column from './column.js';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';
import styles from './style.module.css'

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

const Board = ({ task }) => {

  const [isPopupVisible, setIsPopupVisible] = useState(false);
  const [popupTitle, setPopupTitle] = useState('');
  const [popupAssignee, setPopupAssignee] = useState('');

  const handleKeyDown = (event) => {
    if (event.key === 'Escape') {
      if (isPopupVisible) {
        setIsPopupVisible(false); // Показываем div, если он скрыт
      }
    }
  };

  useEffect(() => {
    window.addEventListener('keydown', handleKeyDown);

    // Убираем обработчик при размонтировании компонента
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [isPopupVisible]);

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
        <Column title="Беклог" tasks={tasks.todo} droppableId={'todo'} popupSetters={[setPopupTitle, setPopupAssignee, setIsPopupVisible]}/>
        <Column title="В процессе" tasks={tasks.inProgress} droppableId={'inProgress'} popupSetters={[setPopupTitle, setPopupAssignee, setIsPopupVisible]}/>
        <Column title="Выполнено" tasks={tasks.done} droppableId={'done'} popupSetters={[setPopupTitle, setPopupAssignee, setIsPopupVisible]}/>
      </div>
      <div>
      {isPopupVisible && (
        <div className={styles.popup}>
        <div className={styles.popupContent}>
          <div className={styles.titlepopup}>
          <h2>{popupTitle}</h2>
          <i onClick={handleClosePopup} class="fa fa-times" aria-hidden="true"></i>
          </div>
          <p>{popupAssignee}</p>
          <div className={styles.textbox}>
            <div className={styles.textbtn}>
              <div className={styles.btnedit}>
              <i class="fa fa-italic" aria-hidden="true"></i>
              </div>
              <div className={styles.btnedit}>
              <i class="fa fa-bold" aria-hidden="true"></i>
              </div>
              <div className={styles.btnedit}>
              <i cclass="fa fa-underline" aria-hidden="true"></i>
              </div>
              <div className={styles.btnedit}>
              <i class="fa fa-link" aria-hidden="true"></i>
              </div>
            </div>
          <input className={styles.texteditor} type="text" id="name" name="name"/>
          </div>
          <p>Приоритет: </p>
          <button className={styles.btn}>Отправить</button>
        </div>
      </div>
      )}
    </div>
    </DragDropContext>
  );
};

export default Board;
