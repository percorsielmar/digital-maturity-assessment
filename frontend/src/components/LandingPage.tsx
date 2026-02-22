import React, { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, useMotionValue, useSpring, useTransform } from 'framer-motion';

// ─── Color Constants ───────────────────────────────────────────────
const COLORS = {
  primary: '#39FF14',       // Neon Wasabi (Agri-Growth)
  secondary: '#00E5E5',     // Electric Blue (Energy-AI)
  background: '#0A102A',    // Deep Space Navy
  neutral: '#E6E7EA',       // Light text
  cardBg: 'rgba(255,255,255,0.05)',
  cardBorder: 'rgba(255,255,255,0.08)',
};

// ─── Portal Data ───────────────────────────────────────────────────
interface PortalCard {
  id: string;
  title: string;
  subtitle: string;
  icon: React.ReactNode;
  route: string;
  accentColor: string;
  glowColor: string;
}

const PORTALS: PortalCard[] = [
  {
    id: 'dma',
    title: 'Maturità Digitale',
    subtitle: 'Assessment per Aziende e PA',
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" className="w-8 h-8">
        <path d="M3 13h2v8H3zM7 9h2v12H7zM11 11h2v10h-2zM15 7h2v14h-2zM19 4h2v17h-2z" strokeLinecap="round" strokeLinejoin="round"/>
      </svg>
    ),
    route: '/maturita-digitale',
    accentColor: COLORS.secondary,
    glowColor: 'rgba(0,229,229,0.4)',
  },
  {
    id: 'iso56002',
    title: 'Audit UNI/PdR 56002',
    subtitle: 'Gestione dell\'Innovazione',
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" className="w-8 h-8">
        <path d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" strokeLinecap="round" strokeLinejoin="round"/>
      </svg>
    ),
    route: '/iso56002',
    accentColor: '#10B981',
    glowColor: 'rgba(16,185,129,0.4)',
  },
  {
    id: 'governance',
    title: 'Governance Trasparente',
    subtitle: 'Formazione e Consulenza PA',
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" className="w-8 h-8">
        <path d="M12 21a9.004 9.004 0 008.716-6.747M12 21a9.004 9.004 0 01-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 017.843 4.582M12 3a8.997 8.997 0 00-7.843 4.582m15.686 0A11.953 11.953 0 0112 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0121 12c0 .778-.099 1.533-.284 2.253m0 0A17.919 17.919 0 0112 16.5a17.92 17.92 0 01-8.716-2.247m0 0A9.015 9.015 0 013 12c0-1.605.42-3.113 1.157-4.418" strokeLinecap="round" strokeLinejoin="round"/>
      </svg>
    ),
    route: '/governance',
    accentColor: '#F59E0B',
    glowColor: 'rgba(245,158,11,0.4)',
  },
  {
    id: 'patto_di_senso',
    title: 'Patto di Senso',
    subtitle: 'Innovazione Sociale e Territoriale',
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" className="w-8 h-8">
        <path d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" strokeLinecap="round" strokeLinejoin="round"/>
      </svg>
    ),
    route: '/patto-di-senso',
    accentColor: '#EC4899',
    glowColor: 'rgba(236,72,153,0.4)',
  },
];

// ─── Cursor Glow Component ─────────────────────────────────────────
const CursorGlow: React.FC = () => {
  const mouseX = useMotionValue(0);
  const mouseY = useMotionValue(0);
  const smoothX = useSpring(mouseX, { damping: 25, stiffness: 150 });
  const smoothY = useSpring(mouseY, { damping: 25, stiffness: 150 });

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      mouseX.set(e.clientX);
      mouseY.set(e.clientY);
    };
    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, [mouseX, mouseY]);

  return (
    <motion.div
      className="pointer-events-none fixed inset-0 z-0"
      style={{
        background: useTransform(
          [smoothX, smoothY],
          ([x, y]) =>
            `radial-gradient(600px circle at ${x}px ${y}px, rgba(57,255,20,0.06), rgba(0,229,229,0.03), transparent 70%)`
        ),
      }}
    />
  );
};

// ─── Animated Mesh Background ──────────────────────────────────────
const MeshBackground: React.FC = () => (
  <div className="fixed inset-0 z-0 overflow-hidden">
    {/* Base background */}
    <div className="absolute inset-0" style={{ background: COLORS.background }} />

    {/* Animated gradient orbs */}
    <motion.div
      className="absolute w-[800px] h-[800px] rounded-full opacity-20"
      style={{
        background: `radial-gradient(circle, ${COLORS.primary}33, transparent 70%)`,
        top: '-20%',
        right: '-10%',
      }}
      animate={{
        x: [0, 50, -30, 0],
        y: [0, -40, 20, 0],
        scale: [1, 1.1, 0.95, 1],
      }}
      transition={{ duration: 20, repeat: Infinity, ease: 'easeInOut' }}
    />
    <motion.div
      className="absolute w-[600px] h-[600px] rounded-full opacity-15"
      style={{
        background: `radial-gradient(circle, ${COLORS.secondary}33, transparent 70%)`,
        bottom: '-15%',
        left: '-5%',
      }}
      animate={{
        x: [0, -40, 30, 0],
        y: [0, 30, -20, 0],
        scale: [1, 0.95, 1.1, 1],
      }}
      transition={{ duration: 25, repeat: Infinity, ease: 'easeInOut' }}
    />
    <motion.div
      className="absolute w-[400px] h-[400px] rounded-full opacity-10"
      style={{
        background: `radial-gradient(circle, ${COLORS.primary}22, ${COLORS.secondary}11, transparent 70%)`,
        top: '40%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
      }}
      animate={{
        scale: [1, 1.2, 0.9, 1],
        rotate: [0, 90, 180, 360],
      }}
      transition={{ duration: 30, repeat: Infinity, ease: 'easeInOut' }}
    />

    {/* Grid overlay */}
    <div
      className="absolute inset-0 opacity-[0.03]"
      style={{
        backgroundImage: `linear-gradient(${COLORS.neutral}15 1px, transparent 1px), linear-gradient(90deg, ${COLORS.neutral}15 1px, transparent 1px)`,
        backgroundSize: '60px 60px',
      }}
    />
  </div>
);

// ─── Data Pulse (Canvas Sinusoidal Wave) ───────────────────────────
const DataPulse: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animationId: number;
    let time = 0;

    const resize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    resize();
    window.addEventListener('resize', resize);

    const draw = () => {
      const { width, height } = canvas;
      ctx.clearRect(0, 0, width, height);
      time += 0.008;

      // Draw multiple layered waves for depth
      const waves = [
        { amp: 40, freq: 0.004, speed: 1.0, yOff: 0.48, color: COLORS.primary, alpha: 0.22, lineW: 1.8 },
        { amp: 25, freq: 0.006, speed: 1.4, yOff: 0.50, color: COLORS.secondary, alpha: 0.16, lineW: 1.5 },
        { amp: 55, freq: 0.003, speed: 0.7, yOff: 0.52, color: COLORS.primary, alpha: 0.12, lineW: 1.2 },
      ];

      for (const wave of waves) {
        const baseY = height * wave.yOff;
        ctx.beginPath();
        ctx.strokeStyle = wave.color;
        ctx.globalAlpha = wave.alpha;
        ctx.lineWidth = wave.lineW;

        for (let x = 0; x <= width; x += 2) {
          // Composite sine: base wave + heartbeat spike
          const base = Math.sin(x * wave.freq + time * wave.speed) * wave.amp;
          // Periodic "heartbeat" spike every ~400px
          const pulse = Math.exp(-Math.pow(((x + time * 60 * wave.speed) % 400) - 200, 2) / 800) * wave.amp * 1.2;
          const y = baseY + base + pulse;

          if (x === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }
        ctx.stroke();

        // Faint glow duplicate
        ctx.globalAlpha = wave.alpha * 0.4;
        ctx.lineWidth = wave.lineW + 3;
        ctx.stroke();
      }

      ctx.globalAlpha = 1;
      animationId = requestAnimationFrame(draw);
    };

    draw();

    return () => {
      cancelAnimationFrame(animationId);
      window.removeEventListener('resize', resize);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 z-[1] pointer-events-none"
      style={{ opacity: 1 }}
    />
  );
};

// ─── AI Streaming Text ─────────────────────────────────────────────
const AI_STATUS_MESSAGES = [
  'Analisi ESG in corso…',
  'Scansione SDG attiva…',
  'Monitoraggio filiera food…',
  'Audit energetico live…',
  'Validazione dati blockchain…',
  'Modello predittivo attivo…',
  'Indice sostenibilità: OK',
  'Nodi IA operativi: 12/12',
];

const AiStreamingText: React.FC = () => {
  const [index, setIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setIndex((prev) => (prev + 1) % AI_STATUS_MESSAGES.length);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <motion.span
      key={index}
      initial={{ opacity: 0, y: 6 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -6 }}
      transition={{ duration: 0.4 }}
      className="text-[10px] tracking-wide"
      style={{ color: `${COLORS.primary}99` }}
    >
      {AI_STATUS_MESSAGES[index]}
    </motion.span>
  );
};

// ─── Navbar ────────────────────────────────────────────────────────
const Navbar: React.FC = () => {
  const navigate = useNavigate();

  return (
    <motion.nav
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.6 }}
      className="relative z-20 flex items-center justify-between px-6 md:px-12 py-5"
    >
      {/* Logo */}
      <div className="flex items-center gap-3">
        <div className="relative w-10 h-10">
          <motion.div
            className="absolute inset-0 rounded-lg"
            style={{
              background: `linear-gradient(135deg, ${COLORS.primary}, ${COLORS.secondary})`,
            }}
            animate={{ rotate: [0, 360] }}
            transition={{ duration: 60, repeat: Infinity, ease: 'linear' }}
          />
          <div
            className="absolute inset-[2px] rounded-[6px] flex items-center justify-center"
            style={{ background: COLORS.background }}
          >
            <span className="text-sm font-bold" style={{ color: COLORS.primary }}>
              AI
            </span>
          </div>
        </div>
        <div>
          <span className="text-lg font-bold" style={{ color: COLORS.neutral }}>
            Rome <span style={{ color: COLORS.primary }}>DIH</span>
          </span>
          <p className="text-[10px] tracking-widest uppercase" style={{ color: `${COLORS.neutral}66` }}>
            Digital Innovation Hub
          </p>
        </div>
      </div>

      <div className="flex items-center gap-4">
        {/* AI Live Status */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.4, duration: 0.6 }}
          className="hidden sm:flex items-center gap-3 px-4 py-2 rounded-lg border"
          style={{
            background: 'rgba(57,255,20,0.04)',
            borderColor: 'rgba(57,255,20,0.12)',
          }}
        >
          {/* Pulsing dot */}
          <span className="relative flex h-2.5 w-2.5">
            <motion.span
              className="absolute inset-0 rounded-full"
              style={{ background: COLORS.primary }}
              animate={{ scale: [1, 1.8, 1], opacity: [0.7, 0, 0.7] }}
              transition={{ duration: 2, repeat: Infinity, ease: 'easeInOut' }}
            />
            <span
              className="relative inline-flex rounded-full h-2.5 w-2.5"
              style={{ background: COLORS.primary }}
            />
          </span>

          {/* Animated data stream */}
          <div className="flex flex-col">
            <span className="text-[10px] font-semibold tracking-wider uppercase" style={{ color: COLORS.primary }}>
              AI Live Status
            </span>
            <div className="flex items-center gap-1.5">
              <AiStreamingText />
            </div>
          </div>

          {/* Mini bar chart animation */}
          <div className="flex items-end gap-[2px] h-4 ml-1">
            {[0, 0.15, 0.3, 0.45, 0.6].map((delay, i) => (
              <motion.div
                key={i}
                className="w-[3px] rounded-full"
                style={{ background: `${COLORS.primary}88` }}
                animate={{ height: ['30%', '100%', '50%', '80%', '30%'] }}
                transition={{
                  duration: 1.5,
                  repeat: Infinity,
                  delay,
                  ease: 'easeInOut',
                }}
              />
            ))}
          </div>
        </motion.div>

        {/* Console Amministrativa link */}
        <motion.button
          onClick={() => navigate('/admin')}
          className="text-xs tracking-wider uppercase px-4 py-2 rounded-lg border transition-all duration-300"
          style={{
            color: `${COLORS.neutral}88`,
            borderColor: `${COLORS.neutral}15`,
            background: 'rgba(255,255,255,0.03)',
          }}
          whileHover={{
            borderColor: `${COLORS.secondary}44`,
            color: COLORS.secondary,
            background: 'rgba(0,229,229,0.05)',
          }}
        >
          Console Amministrativa
        </motion.button>
      </div>
    </motion.nav>
  );
};

// ─── Hero Section ──────────────────────────────────────────────────
const HeroSection: React.FC = () => (
  <section className="relative z-10 text-center px-6 md:px-12 pt-12 md:pt-20 pb-8">
    {/* Badge */}
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.2, duration: 0.6 }}
      className="inline-flex items-center gap-2 px-4 py-2 rounded-full mb-8"
      style={{
        background: 'rgba(57,255,20,0.08)',
        border: '1px solid rgba(57,255,20,0.15)',
      }}
    >
      <motion.div
        className="w-2 h-2 rounded-full"
        style={{ background: COLORS.primary }}
        animate={{ opacity: [1, 0.3, 1] }}
        transition={{ duration: 2, repeat: Infinity }}
      />
      <span className="text-xs tracking-wider uppercase" style={{ color: COLORS.primary }}>
        Piattaforma AI-Powered &bull; Food &bull; Energia &bull; Sostenibilità
      </span>
    </motion.div>

    {/* Main Title */}
    <motion.h1
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.4, duration: 0.7 }}
      className="text-4xl md:text-6xl lg:text-7xl font-extrabold leading-tight max-w-5xl mx-auto mb-6"
    >
      <span style={{ color: COLORS.neutral }}>L'</span>
      <span
        style={{
          background: `linear-gradient(135deg, ${COLORS.secondary}, ${COLORS.primary})`,
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
        }}
      >
        Intelligenza Artificiale
      </span>
      <br />
      <span style={{ color: COLORS.neutral }}>al servizio della </span>
      <span
        style={{
          background: `linear-gradient(135deg, ${COLORS.primary}, ${COLORS.secondary})`,
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
        }}
      >
        Sostenibilità
      </span>
    </motion.h1>

    {/* Subtitle */}
    <motion.p
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.6, duration: 0.6 }}
      className="text-base md:text-lg max-w-2xl mx-auto mb-4 leading-relaxed"
      style={{ color: `${COLORS.neutral}99` }}
    >
      Audit ESG/SDG, Certificazione ISO 56002 e Formazione per la PA.
      <br className="hidden md:block" />
      Food Chain, Agricoltura Sostenibile ed Energia — validati da esperti AI Senior.
    </motion.p>

    {/* Expert badges */}
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.8, duration: 0.6 }}
      className="flex flex-col sm:flex-row items-center justify-center gap-3 mt-6"
    >
      <div
        className="flex items-center gap-2 px-4 py-2 rounded-full text-xs"
        style={{
          background: 'rgba(0,229,229,0.08)',
          border: '1px solid rgba(0,229,229,0.15)',
          color: COLORS.secondary,
        }}
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" className="w-4 h-4">
          <path d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
        Software Architect AI &bull; Data Integrity & Energy
      </div>
      <div
        className="flex items-center gap-2 px-4 py-2 rounded-full text-xs"
        style={{
          background: 'rgba(57,255,20,0.08)',
          border: '1px solid rgba(57,255,20,0.15)',
          color: COLORS.primary,
        }}
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" className="w-4 h-4">
          <path d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
        Validatore Senior AI Developer &bull; GenAI & Compliance
      </div>
    </motion.div>
  </section>
);

// ─── Portal Card Component ─────────────────────────────────────────
const PortalCardComponent: React.FC<{ portal: PortalCard; index: number }> = ({ portal, index }) => {
  const navigate = useNavigate();
  const [isHovered, setIsHovered] = useState(false);

  return (
    <motion.div
      initial={{ opacity: 0, y: 40 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.3 + index * 0.15, duration: 0.6, ease: 'easeOut' }}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      onClick={() => navigate(portal.route)}
      className="relative group cursor-pointer"
    >
      {/* Glow effect on hover */}
      <motion.div
        className="absolute -inset-[1px] rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"
        style={{
          background: `linear-gradient(135deg, ${portal.accentColor}33, transparent, ${portal.accentColor}22)`,
        }}
      />

      {/* Card */}
      <div
        className="relative rounded-2xl p-6 md:p-8 backdrop-blur-xl border transition-all duration-500 h-full"
        style={{
          background: isHovered ? 'rgba(255,255,255,0.08)' : COLORS.cardBg,
          borderColor: isHovered ? `${portal.accentColor}44` : COLORS.cardBorder,
        }}
      >
        {/* Icon container */}
        <motion.div
          className="w-14 h-14 rounded-xl flex items-center justify-center mb-5"
          style={{
            background: `${portal.accentColor}15`,
            color: portal.accentColor,
            border: `1px solid ${portal.accentColor}22`,
          }}
          animate={isHovered ? { scale: 1.1, rotate: 5 } : { scale: 1, rotate: 0 }}
          transition={{ type: 'spring', stiffness: 300, damping: 20 }}
        >
          {portal.icon}
        </motion.div>

        {/* Title */}
        <h3
          className="text-lg font-bold mb-2 transition-colors duration-300"
          style={{ color: isHovered ? portal.accentColor : COLORS.neutral }}
        >
          {portal.title}
        </h3>

        {/* Subtitle */}
        <p className="text-sm mb-6" style={{ color: `${COLORS.neutral}66` }}>
          {portal.subtitle}
        </p>

        {/* Button */}
        <motion.button
          className="w-full py-3 rounded-xl text-sm font-semibold tracking-wide uppercase flex items-center justify-center gap-2 transition-all duration-300"
          style={{
            background: isHovered ? `${portal.accentColor}22` : 'rgba(255,255,255,0.05)',
            color: isHovered ? portal.accentColor : `${COLORS.neutral}99`,
            border: `1px solid ${isHovered ? `${portal.accentColor}44` : 'rgba(255,255,255,0.08)'}`,
            boxShadow: isHovered ? `0 0 20px ${portal.glowColor}` : 'none',
          }}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          Accesso Portale
          <motion.svg
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            className="w-4 h-4"
            animate={isHovered ? { x: 4 } : { x: 0 }}
            transition={{ type: 'spring', stiffness: 300 }}
          >
            <path d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" strokeLinecap="round" strokeLinejoin="round" />
          </motion.svg>
        </motion.button>
      </div>
    </motion.div>
  );
};

// ─── Portals Section ───────────────────────────────────────────────
const PortalsSection: React.FC = () => (
  <section className="relative z-10 px-6 md:px-12 py-12 md:py-16">
    {/* Section header */}
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.2, duration: 0.6 }}
      className="text-center mb-12"
    >
      <h2 className="text-2xl md:text-3xl font-bold mb-3" style={{ color: COLORS.neutral }}>
        Accedi al tuo{' '}
        <span
          style={{
            background: `linear-gradient(135deg, ${COLORS.secondary}, ${COLORS.primary})`,
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
          }}
        >
          Portale
        </span>
      </h2>
      <p className="text-sm" style={{ color: `${COLORS.neutral}66` }}>
        Seleziona il programma di audit o formazione per la tua organizzazione
      </p>
    </motion.div>

    {/* Cards grid */}
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 max-w-6xl mx-auto">
      {PORTALS.map((portal, index) => (
        <PortalCardComponent key={portal.id} portal={portal} index={index} />
      ))}
    </div>
  </section>
);

// ─── Stats Section ─────────────────────────────────────────────────
const StatsSection: React.FC = () => {
  const stats = [
    { value: '108+', label: 'Domande per Audit', color: COLORS.primary },
    { value: '4', label: 'Programmi Attivi', color: COLORS.secondary },
    { value: 'AI', label: 'Report Automatizzati', color: COLORS.primary },
    { value: 'SDG', label: 'Allineamento ONU 2030', color: COLORS.secondary },
  ];

  return (
    <section className="relative z-10 px-6 md:px-12 py-12">
      <div
        className="max-w-5xl mx-auto rounded-2xl backdrop-blur-xl border p-8 md:p-10"
        style={{
          background: COLORS.cardBg,
          borderColor: COLORS.cardBorder,
        }}
      >
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
          {stats.map((stat, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 + i * 0.1, duration: 0.5 }}
              className="text-center"
            >
              <div className="text-3xl md:text-4xl font-extrabold mb-1" style={{ color: stat.color }}>
                {stat.value}
              </div>
              <div className="text-xs tracking-wider uppercase" style={{ color: `${COLORS.neutral}66` }}>
                {stat.label}
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

// ─── Footer ────────────────────────────────────────────────────────
const Footer: React.FC = () => {
  const navigate = useNavigate();

  return (
    <footer className="relative z-10 px-6 md:px-12 py-8 mt-8">
      <div
        className="border-t pt-8 flex flex-col md:flex-row items-center justify-between gap-4"
        style={{ borderColor: `${COLORS.neutral}10` }}
      >
        <div className="flex flex-col items-center md:items-start gap-1">
          <span className="text-sm font-semibold" style={{ color: `${COLORS.neutral}88` }}>
            Rome Digital Innovation Hub
          </span>
          <span className="text-xs" style={{ color: `${COLORS.neutral}44` }}>
            in collaborazione con Il Borgo Urbano &bull; Programma di Trasformazione Digitale
          </span>
        </div>

        <div className="flex items-center gap-6">
          <motion.button
            onClick={() => navigate('/admin')}
            className="text-xs tracking-wider uppercase transition-colors duration-300 flex items-center gap-2"
            style={{ color: `${COLORS.neutral}44` }}
            whileHover={{ color: COLORS.secondary }}
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" className="w-4 h-4">
              <path d="M10.343 3.94c.09-.542.56-.94 1.11-.94h1.093c.55 0 1.02.398 1.11.94l.149.894c.07.424.384.764.78.93.398.164.855.142 1.205-.108l.737-.527a1.125 1.125 0 011.45.12l.773.774c.39.389.44 1.002.12 1.45l-.527.737c-.25.35-.272.806-.107 1.204.165.397.505.71.93.78l.893.15c.543.09.94.56.94 1.109v1.094c0 .55-.397 1.02-.94 1.11l-.893.149c-.425.07-.765.383-.93.78-.165.398-.143.854.107 1.204l.527.738c.32.447.269 1.06-.12 1.45l-.774.773a1.125 1.125 0 01-1.449.12l-.738-.527c-.35-.25-.806-.272-1.204-.107-.397.165-.71.505-.78.929l-.15.894c-.09.542-.56.94-1.11.94h-1.094c-.55 0-1.019-.398-1.11-.94l-.148-.894c-.071-.424-.384-.764-.781-.93-.398-.164-.854-.142-1.204.108l-.738.527c-.447.32-1.06.269-1.45-.12l-.773-.774a1.125 1.125 0 01-.12-1.45l.527-.737c.25-.35.273-.806.108-1.204-.165-.397-.506-.71-.93-.78l-.894-.15c-.542-.09-.94-.56-.94-1.109v-1.094c0-.55.398-1.02.94-1.11l.894-.149c.424-.07.765-.383.93-.78.165-.398.143-.854-.107-1.204l-.527-.738a1.125 1.125 0 01.12-1.45l.773-.773a1.125 1.125 0 011.45-.12l.737.527c.35.25.807.272 1.204.107.397-.165.71-.505.78-.929l.15-.894z" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
            Console Amministrativa
          </motion.button>
          <span className="text-xs" style={{ color: `${COLORS.neutral}22` }}>
            &copy; {new Date().getFullYear()}
          </span>
        </div>
      </div>
    </footer>
  );
};

// ─── Main Landing Page ─────────────────────────────────────────────
const LandingPage: React.FC = () => {
  return (
    <div className="min-h-screen relative" style={{ background: COLORS.background }}>
      <MeshBackground />
      <DataPulse />
      <CursorGlow />
      <div className="relative z-10 flex flex-col min-h-screen">
        <Navbar />
        <main className="flex-1">
          <HeroSection />
          <PortalsSection />
          <StatsSection />
        </main>
        <Footer />
      </div>
    </div>
  );
};

export default LandingPage;
