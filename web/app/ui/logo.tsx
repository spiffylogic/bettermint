import { lusitana } from '@/app/ui/fonts';
import Link from 'next/link';
import Image from 'next/image';

export default function Logo() {
  return (
    <div className={`${lusitana.className} flex flex-row items-center leading-none text-white`}>
        <Link href="/">
            <Image src="/mint.svg"  width={128} height={128} alt="Logo" />
        </Link>
        <p className="text-[44px]">Bettermint</p>
    </div>
  );
}
