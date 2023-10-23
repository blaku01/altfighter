import { useState, useEffect } from 'react';
import MissionsComponent from '/components/missions'
import SingleMissionComponent from '/components/mission'
import { useRouter } from 'next/router';

function Missions(res, req) {
  const router = useRouter()
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
  if (Object.keys(data.missions).length == 6) {
      router.push(`/missions/${data.missions.id}`)
  } else {
    return (
      <MissionsComponent missions={data.missions} />
    )
  }
}


export default Missions;
