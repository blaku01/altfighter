
import { useRouter } from 'next/router'
function cancelMission(id) {
    fetch('/api/missions/cancel/' + id.toString(), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    })
  }
function SingleMissionComponent({ mission }) {
    const router = useRouter()
    return (

        <div className={`col-span-6 w-[100%] flex items-center justify-center`} style={{ zIndex: 1 }}>
            <p>{mission.id} {mission.total_time}</p>
            <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" type="button" onClick={() => {cancelMission(mission.id); router.push('/missions')}}>cancel missions</button>
        </div>
    )
}

export default SingleMissionComponent;