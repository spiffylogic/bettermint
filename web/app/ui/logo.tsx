import { lusitana } from '@/app/ui/fonts';
import Link from 'next/link';
import Image from 'next/image';

export default function Logo() {
  return (
    <div className={`${lusitana.className} flex flex-row items-center leading-none text-white`}>
        <Image src="/mint.svg"  width={128} height={128} alt="Logo" />
        <p className="text-[32px]">Bettermint</p>
    </div>
  );
}
