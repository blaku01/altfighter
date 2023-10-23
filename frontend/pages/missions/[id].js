import { useState, useEffect } from 'react';
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
  if (isLoading) return <></>
  if (!data) return <></>
  console.log(data.missions, Object.keys(data.missions).length)
  if (Object.keys(data.missions).length == 6) {
    return (
      <SingleMissionComponent mission={data.missions} />
    )
  } else {
    return <></>
  }}


  export default Missions;
