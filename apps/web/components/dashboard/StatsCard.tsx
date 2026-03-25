interface StatsCardProps {
  title: string;
  value: number | string;
  description?: string;
  icon: React.ReactNode;
  accent?: boolean;
}

export default function StatsCard({ title, value, description, icon, accent = false }: StatsCardProps) {
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5 flex items-start gap-4">
      <div className={`w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0 ${accent ? 'bg-orange-50 text-orange-500' : 'bg-gray-100 text-gray-500'}`}>
        {icon}
      </div>
      <div className="min-w-0">
        <p className="text-sm text-gray-500 truncate">{title}</p>
        <p className="text-2xl font-bold text-gray-900 mt-0.5">{value}</p>
        {description && (
          <p className="text-xs text-gray-400 mt-0.5">{description}</p>
        )}
      </div>
    </div>
  );
}
