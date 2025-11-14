import React, {useState} from 'react'

export default function CreateTask({onCreate, systemsA, systemsB}){
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [systemA, setSystemA] = useState('')
  const [systemB, setSystemB] = useState('')
  const [direction, setDirection] = useState('a_to_b')
  const [schedule, setSchedule] = useState(false)
  const [interval, setInterval] = useState('')
  const [loading, setLoading] = useState(false)

  async function submit(e){
    e.preventDefault()
    setLoading(true)
    try{
      const payload = {
        name,
        description,
        system_a: systemA,
        system_b: systemB,
        direction,
        schedule_enabled: schedule,
        schedule_interval: interval ? parseInt(interval,10) : null,
      }
      const created = await onCreate(payload)
      // очистим форму
      setName('')
      setDescription('')
      setSystemA('')
      setSystemB('')
      setInterval('')
      alert('Задача создана')
    }catch(err){
      console.error(err)
      alert('Ошибка при создании: ' + err.message)
    }finally{
      setLoading(false)
    }
  }

  return (
    <form className="create-form" onSubmit={submit}>
      <h2>Создать задачу интеграции</h2>
      <label>Название<br/><input value={name} onChange={e=>setName(e.target.value)} required/></label>
      <label>Описание<br/><textarea value={description} onChange={e=>setDescription(e.target.value)} /></label>

      <label>Система A<br/>
        <select value={systemA} onChange={e=>setSystemA(e.target.value)} required>
          <option value="">— выберите —</option>
          {systemsA.map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
        </select>
      </label>

      <label>Система B<br/>
        <select value={systemB} onChange={e=>setSystemB(e.target.value)} required>
          <option value="">— выберите —</option>
          {systemsB.map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
        </select>
      </label>

      <label>Направление<br/>
        <select value={direction} onChange={e=>setDirection(e.target.value)}>
          <option value="a_to_b">A → B</option>
          <option value="b_to_a">B → A</option>
          <option value="bidirectional">Двусторонняя</option>
        </select>
      </label>

      <label><input type="checkbox" checked={schedule} onChange={e=>setSchedule(e.target.checked)} /> Включить расписание</label>
      {schedule && <label>Интервал (минуты)<br/><input value={interval} onChange={e=>setInterval(e.target.value)} type="number" min="1"/></label>}

      <button type="submit" disabled={loading}>{loading ? 'Создаю...' : 'Создать'}</button>
    </form>
  )
}
