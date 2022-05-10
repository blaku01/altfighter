
import Image from "next/image";
import { useRouter } from 'next/router'
import NavbarItem from "./navbarItem";
import useSWR from 'swr'
const fetcher = (...args) => fetch(...args).then((res) => res.json())


function UserComponent() {
    console.log('fetching...')
    const router = useRouter()
    const { data, error } = useSWR('/api/user_character', fetcher)
    if (router.pathname == '/login') return <></>
    if (error) {
        router.push('/login')
        return <></>
    }
    if (!data) return <div>Loading...</div>
    return (
        <div className="w-[45vw] h-[90vh] my-[5vh] flex items-center justify-center border" style={{ zIndex: 1 }}>
            {/* user info */}
            <div className="self-center border flex flex-col w-[90%] h-[100%] items-center justify-center">
                <div className="w-[100%] h-[60%] flex border ">
                    <div className="w-[25%] h-full flex flex-col items-center border">
                        <div className="w-[90%] h-[30%] border"></div>
                        <div className="w-[90%] h-[30%] border"></div>
                        <div className="w-[90%] h-[30%] border"></div>
                    </div>
                    <div className="w-[50%] h-full flex flex-col items-center border">
                        <div className="w-[80%] h-[60%] border"></div>
                        <div className="w-[80%] h-[40%] flex items-center border">
                            <div className="w-[50%] h-[70%] border"></div>
                            <div className="w-[50%] h-[70%] border"></div>
                        </div>
                    </div>
                    <div className="w-[25%] h-full flex flex-col items-center border">
                        <div className="w-[90%] h-[30%] border"></div>
                        <div className="w-[90%] h-[30%] border"></div>
                        <div className="w-[90%] h-[30%] border"></div>
                    </div>
                </div>
                <div className="w-[100%] h-[40%] flex flex-wrap items-center justify-center border">
                    <div className="w-[25%] h-[40%] mx-[3%] border"></div>
                    <div className="w-[25%] h-[40%] mx-[3%] border"></div>
                    <div className="w-[25%] h-[40%] mx-[3%] border"></div>
                    <div className="w-[25%] h-[40%] mx-[3%] border"></div>
                    <div className="w-[25%] h-[40%] mx-[3%] border"></div>
                    <div className="w-[25%] h-[40%] mx-[3%] border"></div>
                </div>
            </div>
        </div>
    )
}

export default UserComponent;