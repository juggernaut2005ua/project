import React, {useEffect, useState} from 'react'
import api from '../api'

export default function CoursesList(){
  const [courses, setCourses] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(()=>{ (async ()=>{
    try{
      const res = await api.fetchList('courses')
      // API returns { results: [...] }
      setCourses(res.results || [])
    }catch(e){
      console.error(e)
    }finally{ setLoading(false) }
  })() }, [])

  if(loading) return <p>Загрузка курсов...</p>
  if(!courses.length) return <p>Курсы не найдены.</p>

  return (
    <section className="courses">
      <h2>Курсы</h2>
      <ul>
        {courses.map(c => (
          <li key={c.id}>
            <strong>{c.title}</strong> — {c.description} <em>({c.lessons} уроков)</em>
          </li>
        ))}
      </ul>
    </section>
  )
}
