
import Image from "next/image";
import { useRouter } from 'next/router'
import NavbarItem from "./navbarItem";
import useSWR from 'swr'
const fetcher = (...args) => fetch(...args).then((res) => res.json())


function Navbar() {
    const router = useRouter()
    if (router.pathname == '/login') return <></>
    const { data, error } = useSWR('/api/user_character', fetcher)
    if (error) {
        router.push('/login')
        return <></>
    }
    if (!data) return <div>Loading...</div>
    if (data.character.detail == "Not found.") {
        router.push('/login')
        return <></>
    }
    return (
        <div className="w-fit h-[90vh] my-[5vh] bg-black/50 rounded-[5px] flex flex-col " style={{ zIndex: 1 }}>
            {/* user info */}
            <div className="self-center flex w-[90%] items-center">
                <div className=" sm:flex flex-col text-white/80   space-y-0 hidden ">
                    <div className=" text-center font-[700]">{data.character.nickname}</div>
                    <progress className="h-[5px] w-8em" max="100" value={(data.character.current_exp / Math.pow(data.character.level, 3) * 100)}></progress>
                    <div className="text-center">level {data.character.level}</div>
                </div>
            </div>
            <hr className="text-gray-900 border-1 w-[100%]" />

            {/* Links */}
            <ul className="mt-2 flex flex-col h-[100%]">
                <NavbarItem action='fight' />
                <NavbarItem action='missions' />
                <NavbarItem action='shop' />
                <NavbarItem action='leaderboard' />
                <NavbarItem action='logout' is_icon={false} />
            </ul>

        </div>
    )
}

export default Navbar;