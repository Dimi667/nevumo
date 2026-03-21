'use client';
import Link from "next/link";

interface ActionCardProps {
  href: string;
  label: string;
  subtext?: string;
}

export const ActionCard = ({ href, label, subtext }: ActionCardProps) => {
  return (
    <Link 
      href={href} 
      style={{ padding: '24px 32px' }}
      className="group block w-full bg-white border border-[#eee] rounded-[20px] no-underline transition-all duration-300 hover:border-primary hover:shadow-lg active:scale-[0.98]"
    >
      <div className="flex justify-between items-center" style={{ marginBottom: '4px' }}>
        <span className="text-[17px] font-bold text-[#171717] group-hover:text-primary transition-colors">
          {label}
        </span>
        <span className="text-primary text-xl transition-transform group-hover:translate-x-1">
          →
        </span>
      </div>
      
      {subtext && (
        <p className="text-[14px] text-[#666] leading-snug pr-4 font-medium">
          {subtext}
        </p>
      )}
    </Link>
  );
};