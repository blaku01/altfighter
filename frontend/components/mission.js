
import { useRouter } from 'next/router'
import { useEffect, useState } from 'react';
import Image from 'next/image'

function SingleMissionComponent({ mission }) {
  const router = useRouter()
  if (Object.keys(mission).length == 3) {
    router.push('/missions')
  }
  const missionTimeSecs = 60 * parseInt(mission.time.substr(3,2)) + parseInt(mission.time.substr(6,2))
  const [totalSecondsLeft, setTotalSecondsLeft] = useState(mission.total_time)
  const [secondsLeft, setSecondsLeft] = useState(mission.total_time % 60)
  const [minutesLeft, setMinutesLeft] = useState((mission.total_time - secondsLeft) / 60)
  useEffect(() => {
    const id = setInterval(() => {
      setTotalSecondsLeft(totalSecondsLeft - 1)
      setSecondsLeft(secondsLeft - 1)
      if (secondsLeft == 0) {
        setSecondsLeft(59)
        setMinutesLeft(minutesLeft - 1)
      }
      if (minutesLeft == 0 && secondsLeft == 0) {
        router.push('/missions')
      }
    }, 1000);
    return () => clearInterval(id);
  }, [secondsLeft, minutesLeft])

  const cancelMission = (e, id) => {
    console.log('aa')
    fetch('/api/missions/cancel/' + id.toString(), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    })
    router.push('/missions')
  }
  return (

    <div className={`col-span-6 w-[100%] flex items-center justify-center text-white`} style={{ zIndex: 1 }}>
      <div className='relative w-[80vmin] h-[60vmin] flex flex-center flex-col border'>
        <Image
          src="/mission_road.png"
          alt="Picture of the author"
          layout='fill'
          style={{ zIndex: -1 }}
        />
        <div className='w-[100%] h-[70%] flex justify-center text-5xl pt-[10%] text-black'>
          <h1>{mission.name}</h1>
        </div>
        <div className='w-[100%] h-[30%] flex flex-col justify-around items-center'>
          <div className='relative w-[80%] h-[10%] bg-zinc-700'>
            <div className='absolute w-[100%] h-[100%] flex items-center justify-center'>
            <p className='font-bold '>{minutesLeft}:{(secondsLeft.toString().length == 1) ? `0${secondsLeft}` : secondsLeft} / {mission.time.substr(3,5)}</p>
            </div>
            <div className={`h-full bg-green-400`} style={{width: `${(parseInt((missionTimeSecs - totalSecondsLeft) * 100 / missionTimeSecs))}%`}}>
            </div>
          </div>
          <button className="w-[10%] h-[15%] bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline flex items-center justify-center" style={{zIndex: 1}} type="button" onClick={(e) => { cancelMission(e, mission.id) }}>cancel</button>
        </div>
      </div>
    </div>
  )
}

export default SingleMissionComponent;
