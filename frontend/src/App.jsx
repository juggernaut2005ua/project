import React, {useEffect, useState} from 'react'
import api from './api'
import TasksList from './components/TasksList'
import CreateTask from './components/CreateTask'
import Nav from './components/Nav'
import CoursesList from './components/CoursesList'

export default function App(){
  const [tasks, setTasks] = useState([])
  const [systemsA, setSystemsA] = useState([])
  const [systemsB, setSystemsB] = useState([])
  const [loading, setLoading] = useState(true)

  async function loadAll(){
    setLoading(true)
    try{
      const [t, a, b] = await Promise.all([
        api.fetchList('tasks'),
        api.fetchList('system-a'),
        api.fetchList('system-b'),
      ])
      setTasks(t)
      setSystemsA(a)
      setSystemsB(b)
    }catch(err){
      console.error('Ошибка загрузки:', err)
      alert('Ошибка при загрузке данных — посмотрите консоль')
    }finally{
      setLoading(false)
    }
  }

  useEffect(()=>{ loadAll() }, [])

  async function handleCreateTask(payload){
    const created = await api.create('tasks', payload)
    // обновим список
    setTasks(prev => [created, ...prev])
  }

  return (
    <div className="app">
      <Nav />
      <main>
        <h1>KodKids — платформа для детей</h1>
        {loading ? <p>Загрузка...</p> : (
          <>
            <section>
              <h2>Интеграции — задачи</h2>
              <CreateTask onCreate={handleCreateTask} systemsA={systemsA} systemsB={systemsB} />
              <TasksList tasks={tasks} />
            </section>
            <CoursesList />
          </>
        )}
      </main>
    </div>
  )
}
