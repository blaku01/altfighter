import {useEffect } from 'react';
import { useRouter } from 'next/router'

function Logout(res, req) {
    useEffect(() => {
      fetch('/api/auth/logout', {method: 'POST',})}, [])
    const router = useRouter();
    router.push('/login')
    return (<></>)
}

export default Logout;
