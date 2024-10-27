import React, { useEffect, useState } from 'react';
import Column from './column.js';
import { DragDropContext} from 'react-beautiful-dnd';
import styles from './style.module.css'


const Board = ( recipes ) => {
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

  const [tasks, setTasks] = useState(recipes);
  const [todo_tasks, setTodoTasks] = useState(tasks.recipes.filter((task) => task.status === 'todo'));
  const [in_p_tasks, setInProcessTasks] = useState(tasks.recipes.filter((task) => task.status === 'in_p'));
  const [done_tasks, setDoneTasks] = useState(tasks.recipes.filter((task) => task.status === 'done'));
  const [tasksDict, setTasksDict] = useState({
    'todo': todo_tasks,
    'inProgress': in_p_tasks,
    'done': done_tasks
  });

  useEffect(() => {
    setTasks(recipes)
  }, [recipes])

  useEffect(() => {
    setTodoTasks(tasks.recipes.filter((task) => task.status === 'todo'))
    setInProcessTasks(tasks.recipes.filter((task) => task.status === 'in_p'))
    setDoneTasks(tasks.recipes.filter((task) => task.status === 'done'))
  }, [tasks])


  const onDragEnd = (result) => {
    if (!result.destination) return;

    const { source, destination } = result;

    if (source.droppableId !== destination.droppableId) {
      const sourceTasks = Array.from(tasksDict[source.droppableId]);

      const destinationTasks = Array.from(tasksDict[destination.droppableId]);

      const movedTask = sourceTasks.splice(source.index, 1);

      destinationTasks.splice(destination.index, 0, movedTask);

      setTasksDict((prevTasks) => ({
        ...prevTasks,
        [source.droppableId]: sourceTasks,
        [destination.droppableId]: destinationTasks,
      }));
      console.log(tasksDict)
    }
  };
  const popupSetters = [setPopupTitle, setPopupAssignee, setIsPopupVisible]

  return (
    <DragDropContext onDragEnd={onDragEnd}>
      <div className={styles.board}>
        <Column title="Беклог" tasks={todo_tasks} droppableId={'todo'} popupSetters={popupSetters}/>
        <Column title="В процессе" tasks={in_p_tasks} droppableId={'inProgress'} popupSetters={popupSetters}/>
        <Column title="Выполнено" tasks={done_tasks} droppableId={'done'} popupSetters={[setPopupTitle, setPopupAssignee, setIsPopupVisible]}/>
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
