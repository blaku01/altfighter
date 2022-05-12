import { useState, useEffect } from 'react';
import MissionsComponent from '/components/missions'
import SingleMissionComponent from '/components/mission'


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
  console.log(data.missions, Object.keys(data.missions).length)
  if (Object.keys(data.missions).length == 6) {
    return (
      <SingleMissionComponent mission={data.missions} />
    )
  } else {
    return (
      <MissionsComponent missions={data.missions} />
    )
  }
}


export default Missions;