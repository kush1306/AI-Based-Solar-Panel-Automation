"use client";

import { motion } from "framer-motion";

export function SolarFactoryBanner() {
  return (
    <div className="overflow-hidden rounded-retro border-[3px] border-outline shadow-retro">
      <div className="flex items-center justify-between border-b-[3px] border-outline bg-pink px-3 py-2">
        <span className="font-pixel text-[8px] uppercase">Solar Factory</span>
        <span className="h-2 w-2 animate-pulse rounded-full border-2 border-outline bg-green-500" />
      </div>
      <div className="relative h-52 overflow-hidden bg-sky">
        {/* Clouds */}
        <motion.div
          animate={{ x: [0, 15, 0] }}
          transition={{ repeat: Infinity, duration: 6, ease: "easeInOut" }}
          className="absolute left-[8%] top-4 h-6 w-16 rounded-full border-2 border-outline bg-white"
        />
        <motion.div
          animate={{ x: [0, -12, 0] }}
          transition={{ repeat: Infinity, duration: 8, ease: "easeInOut" }}
          className="absolute right-[12%] top-3 h-7 w-20 rounded-full border-2 border-outline bg-white"
        />

        {/* Sun */}
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ repeat: Infinity, duration: 20, ease: "linear" }}
          className="absolute right-[6%] top-2 text-4xl"
        >
          😊
        </motion.div>

        {/* Ground */}
        <div className="absolute bottom-0 left-0 right-0 h-10 border-t-[3px] border-outline bg-sage" />

        {/* Trees */}
        <div className="absolute bottom-8 left-[5%] text-2xl">🌳</div>
        <div className="absolute bottom-8 right-[8%] text-xl">🌲</div>

        {/* Tiny buildings */}
        <div className="absolute bottom-10 left-[14%] h-10 w-7 border-2 border-outline bg-pink" />
        <div className="absolute bottom-10 right-[14%] h-12 w-6 border-2 border-outline bg-orange" />

        {/* Factory */}
        <div className="absolute bottom-10 left-1/2 -translate-x-1/2">
          <div className="relative">
            {/* Chimneys */}
            <div className="absolute -top-10 left-4 h-10 w-4 border-2 border-outline bg-gray-500">
              <motion.div animate={{ y: [-4, -16], opacity: [0.8, 0] }} transition={{ repeat: Infinity, duration: 2 }} className="absolute -top-2 left-0 h-3 w-3 rounded-full border border-outline bg-white" />
            </div>
            <div className="absolute -top-8 right-6 h-8 w-4 border-2 border-outline bg-gray-500">
              <motion.div animate={{ y: [-4, -14], opacity: [0.8, 0] }} transition={{ repeat: Infinity, duration: 2, delay: 0.8 }} className="absolute -top-2 left-0 h-3 w-3 rounded-full border border-outline bg-white" />
            </div>

            {/* Main building */}
            <div className="relative h-24 w-52 border-[3px] border-outline bg-butter">
              <p className="absolute left-1/2 top-2 -translate-x-1/2 font-pixel text-[6px]">SOLAR FACTORY</p>
              <div className="absolute left-1/2 top-8 flex h-10 w-20 -translate-x-1/2 gap-1 border-2 border-outline bg-gray-900 p-1">
                {[40, 70, 55, 90].map((h, i) => (
                  <div key={i} className="flex-1 self-end border border-gray-600 bg-sage" style={{ height: `${h}%` }} />
                ))}
              </div>
              <div className="absolute bottom-2 left-4 h-5 w-5 border-2 border-outline bg-sky" />
              <div className="absolute bottom-2 right-4 h-5 w-5 border-2 border-outline bg-sky" />
            </div>

            {/* Pipes */}
            <div className="absolute -left-8 bottom-6 h-2 w-10 border-2 border-outline bg-orange" />
            <div className="absolute -right-6 bottom-10 h-8 w-2 border-2 border-outline bg-pink" />
            <div className="absolute right-0 top-4 h-2 w-8 border-2 border-outline bg-sky" />

            {/* Conveyor */}
            <motion.div
              animate={{ backgroundPosition: ["0px 0px", "40px 0px"] }}
              transition={{ repeat: Infinity, duration: 1.5, ease: "linear" }}
              className="absolute -bottom-3 left-2 right-2 flex h-4 gap-1 overflow-hidden border-2 border-outline"
              style={{ background: "repeating-linear-gradient(90deg, #666 0, #666 8px, #888 8px, #888 16px)" }}
            >
              {[...Array(6)].map((_, i) => (
                <div key={i} className="my-0.5 h-2.5 w-5 shrink-0 border border-outline bg-blue-500" />
              ))}
            </motion.div>

            {/* Panel stack */}
            <div className="absolute -left-6 bottom-4 flex flex-col gap-0.5">
              {[...Array(3)].map((_, i) => (
                <div key={i} className="h-2 w-5 -rotate-12 border border-outline bg-blue-500" />
              ))}
            </div>

            {/* Machine */}
            <div className="absolute -right-8 bottom-4 flex h-10 w-10 items-center justify-center border-2 border-outline bg-pink">
              <motion.span animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 3, ease: "linear" }}>⚙️</motion.span>
              <span className="absolute -right-1 -top-1 h-2 w-2 animate-pulse rounded-full border border-outline bg-green-500" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
