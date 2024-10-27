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
  console.log(recipes.recipes[0].status)
  const todoTasks = recipes.recipes.filter((task) => task.status === 'todo')
  const inProcessTasks = recipes.recipes.filter((task) => task.status === 'in_p')
  const doneTasks = recipes.recipes.filter((task) => task.status === 'done')

  const [tasksDict, setTasksDict] = useState({
    'todo': todoTasks,
    'inProgress': inProcessTasks,
    'done': doneTasks
  });
  console.log(tasksDict)
  // useEffect(() => {
  //   setTasks(recipes)
  // }, [recipes])

  // useEffect(() => {
  //   setTodoTasks(tasks.recipes.filter((task) => task.status === 'todo'))
  //   setInProcessTasks(tasks.recipes.filter((task) => task.status === 'in_p'))
  //   setDoneTasks(tasks.recipes.filter((task) => task.status === 'done'))
  // }, [tasks])


  const onDragEnd = (result) => {
    if (!result.destination) return;

    const { source, destination } = result;

    if (source.droppableId !== destination.droppableId) {
      console.log(source.droppableId)
      console.log(tasksDict)
      console.log(tasksDict[source.droppableId])
      const sourceTasks = Array.from(tasksDict[source.droppableId]);
      const destinationTasks = Array.from(tasksDict[destination.droppableId]);
      const movedTask = sourceTasks.splice(source.index, 1);
      movedTask.status = destination.droppableId
      destinationTasks.splice(destination.index, 0, movedTask);
      console.log(sourceTasks)
      console.log(destinationTasks)
      console.log(movedTask)

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
        <Column title="Беклог" tasks={todoTasks} droppableId={'todo'} popupSetters={popupSetters}/>
        <Column title="В процессе" tasks={inProcessTasks} droppableId={'inProgress'} popupSetters={popupSetters}/>
        <Column title="Выполнено" tasks={doneTasks} droppableId={'done'} popupSetters={[setPopupTitle, setPopupAssignee, setIsPopupVisible]}/>
      </div>
      <div>
      {isPopupVisible && (
        <div className={styles.popup}>
        <div className={styles.popupContent}>
          <div className={styles.titlepopup}>
          <h2>{popupTitle}</h2>
          <i onClick={handleClosePopup} className={"fa fa-times"} aria-hidden="true"></i>
          </div>
          <p>{popupAssignee}</p>
          <div className={styles.textbox}>
            <div className={styles.textbtn}>
              <div className={styles.btnedit}>
              <i className={"fa fa-italic"} aria-hidden="true"></i>
              </div>
              <div className={styles.btnedit}>
              <i className={"fa fa-bold"} aria-hidden="true"></i>
              </div>
              <div className={styles.btnedit}>
              <i className={"fa fa-underline"} aria-hidden="true"></i>
              </div>
              <div className={styles.btnedit}>
              <i className={"fa fa-link"} aria-hidden="true"></i>
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
