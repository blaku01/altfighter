
import Image from "next/image";
import Link from 'next/link'
import { useRouter } from 'next/router'

function startMission(id) {
  fetch('/api/missions/start/' + id.toString(), {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
  })
}

function MissionsComponent({ missions }) {
  const router = useRouter()
  return (
    <div className={`col-span-6 w-[100%] flex items-center justify-center`} style={{ zIndex: 1 }}>
      <div className='w-[55vmin] h-[80vmin] flex justify-around'>
        <div className='relative w-full h-full flex items-center justify-center'>
          <Image
            src='/do-gry.jpeg'
            className="w-full h-full  bg-no-repeat bg-cover bg-left rounded-md"
            layout="fill"
            style={{ zIndex: -1 }} />
          <div className='w-[60%] h-[60%] mt-[20%] flex flex-row-reverse flex-wrap text-white'>
            <div className='w-[50%] h-[50%] -rotate-6  flex flex-col items-center justify-center cursor-pointer rounded border-stone-400 hover:border text-[calc(7px+0.8vw)]'  onClick={() => {startMission(missions[0].id); router.push('/missions')}}>
              <p className='text-red-200'>{missions[0].name}</p>
              <p>{missions[0].time}</p>
              <p>gold: {missions[0].currency}</p>
              <p>exp: {missions[0].exp}</p>
            </div>
            <div className='w-[50%] h-[50%]'>
              <div className='w-full h-full rotate-6 mt-[40%] flex flex-col items-center justify-center cursor-pointer rounded border-stone-400	hover:border text-[calc(7px+0.8vw)]' onClick={() => {startMission(missions[1].id); router.push('/missions')}}>
                <p className='text-red-200'>{missions[1].name}</p>
                <p>{missions[1].time}</p>
                <p>gold: {missions[1].currency}</p>
                <p>exp: {missions[1].exp}</p>
              </div>
            </div>
            <div className='w-[50%] h-[50%] mr-[4%] -rotate-6 flex flex-col items-center justify-center cursor-pointer rounded border-stone-400	hover:border text-[calc(7px+0.8vw)]' onClick={() => {startMission(missions[2].id); router.push('/missions')}}>
              <p className='text-red-200'>{missions[2].name}</p>
              <p>{missions[2].time}</p>
              <p>gold: {missions[2].currency}</p>
              <p>exp: {missions[2].exp}</p>
            </div>
          </div>
        </div>


      </div>

    </div>
  )
}

export default MissionsComponent;