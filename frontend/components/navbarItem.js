
import Image from "next/image";
import Link from 'next/link'

function NavbarItem({action, is_icon=true}) {
    const icon_size= 60
    let icon
    if (is_icon){
        icon = <Image layout='fixed' width={icon_size} height={icon_size} src={`/icons/${action}.png`} className='group-hover:text-white'/>
    }
    return(
    <li className="flex text-white/80 items-center space-x-2  hover:bg-white/10 hover:cursor-pointer w-[90%] mx-auto rounded-[15px] p-2 group relative">
        {icon}
        <Link href={action}>
        <span className="text-base group-hover:text-white font-[600] hidden sm:inline">{action}</span>
        </Link>
    </li>
    )
}

export default NavbarItem;