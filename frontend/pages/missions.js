import { useState, useEffect } from 'react';


function Missions(res, req) {
  const [data, setData] = useState(null)
  const [isLoading, setLoading] = useState(false)
  useEffect(() => {
    setLoading(true)
    fetch('/api/missions/')
      .then((res) => res.json())
      .then((data) => {
        setData(data)
        setLoading(false)
      })
  }, [])
  if (isLoading) return <p>Loading...</p>
  if (!data) return <p>No profile data</p>
  return (

    <div className={`col-span-6 flex items-center justify-center	mr-[14.28vw]`} style={{ zIndex: 1 }}>
      <ul>{data.missions.map((mission, index) => {
        return <li>{mission.id} {mission.name} {mission.exp} {mission.currency}</li>
      })}
      </ul>
    </div>
  )
}


export default Missions;

