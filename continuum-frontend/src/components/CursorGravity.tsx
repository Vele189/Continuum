import React, { useEffect, useRef } from 'react';

interface CursorGravityProps {
    isVacuumActive?: boolean;
}

interface Particle {
    x: number;
    y: number;
    vx: number;
    vy: number;
    radius: number;
    originalRadius: number;
    color: string;
    originalX: number;
    originalY: number;
    friction: number;
    springFactor: number;
    update: () => void;
    draw: () => void;
}

class ParticleImpl implements Particle {
    x: number;
    y: number;
    vx: number;
    vy: number;
    radius: number;
    originalRadius: number;
    color: string;
    originalX: number;
    originalY: number;
    friction: number;
    springFactor: number;
    private ctx: CanvasRenderingContext2D | null;
    private width: number;
    private height: number;
    private mouseRef: React.MutableRefObject<{ x: number; y: number }>;
    private isVacuumActiveRef: React.MutableRefObject<boolean>;
    private CURSOR_RADIUS: number;
    private MAX_VELOCITY: number;

    constructor(
        x: number,
        y: number,
        ctx: CanvasRenderingContext2D | null,
        width: number,
        height: number,
        mouseRef: React.MutableRefObject<{ x: number; y: number }>,
        isVacuumActiveRef: React.MutableRefObject<boolean>,
        CURSOR_RADIUS: number,
        MAX_VELOCITY: number
    ) {
        this.x = x;
        this.y = y;
        this.originalX = x;
        this.originalY = y;
        this.vx = 0;
        this.vy = 0;
        this.originalRadius = Math.random() * 2 + 1;
        this.radius = this.originalRadius;
        const colors = ['#4285F4', '#EA4335', '#FBBC05', '#34A853', '#A0C3FF', '#FF9E9E'];
        this.color = colors[Math.floor(Math.random() * colors.length)];
        this.friction = 0.9 + Math.random() * 0.05;
        this.springFactor = 0.01 + Math.random() * 0.02;
        this.ctx = ctx;
        this.width = width;
        this.height = height;
        this.mouseRef = mouseRef;
        this.isVacuumActiveRef = isVacuumActiveRef;
        this.CURSOR_RADIUS = CURSOR_RADIUS;
        this.MAX_VELOCITY = MAX_VELOCITY;
    }

    update() {
        const dx = this.mouseRef.current.x - this.x;
        const dy = this.mouseRef.current.y - this.y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (this.isVacuumActiveRef.current) {
            // Global Vacuum Mode
            const angle = Math.atan2(dy, dx);
            const force = 0.1; // Drastically reduced for gentle suction

            this.vx += Math.cos(angle) * force;
            this.vy += Math.sin(angle) * force;

            this.vx *= 0.95;
            this.vy *= 0.95;

            // "Caught" effect - slow down when close, don't shrink
            // Prevent collapsing to single point by adding short-range repulsion
            if (dist < 30) {
                this.vx *= 0.7;
                this.vy *= 0.7;
                // Push away slightly if TOO close
                if (dist < 10) {
                    this.vx -= Math.cos(angle) * 2;
                    this.vy -= Math.sin(angle) * 2;
                }
            }
        } else {
            // Normal Mode
            // Restore radius slowly
            if (this.radius < this.originalRadius) {
                this.radius += 0.1;
            }

            // Return to original position (homing)
            const dxHome = this.originalX - this.x;
            const dyHome = this.originalY - this.y;

            this.vx += dxHome * this.springFactor;
            this.vy += dyHome * this.springFactor;

            // Mouse repulsion/attraction in normal mode
            if (dist < this.CURSOR_RADIUS) {
                const force = (this.CURSOR_RADIUS - dist) / this.CURSOR_RADIUS;
                const angle = Math.atan2(dy, dx);
                const fx = Math.cos(angle) * force * 2;
                const fy = Math.sin(angle) * force * 2;

                this.vx += fx;
                this.vy += fy;
            }

            this.vx *= 0.90; // Slightly more friction for stable return
            this.vy *= 0.90;
        }

        // Clamp velocity
        const speed = Math.sqrt(this.vx * this.vx + this.vy * this.vy);
        const limit = this.isVacuumActiveRef.current ? 4 : this.MAX_VELOCITY; // Slower speed limit for vacuum
        if (speed > limit) {
            const ratio = limit / speed;
            this.vx *= ratio;
            this.vy *= ratio;
        }

        this.x += this.vx;
        this.y += this.vy;

        // Bounce off walls (only if NOT vacuuming)
        if (!this.isVacuumActiveRef.current) {
            if (this.x < 0 || this.x > this.width) this.vx *= -1;
            if (this.y < 0 || this.y > this.height) this.vy *= -1;
        }
    }

    draw() {
        if (!this.ctx || this.radius <= 0) return;
        this.ctx.beginPath();
        this.ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        this.ctx.fillStyle = this.color;
        this.ctx.fill();
        this.ctx.closePath();
    }
}

const CursorGravity = ({ isVacuumActive = false }: CursorGravityProps) => {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const isVacuumActiveRef = useRef(isVacuumActive);
    const particlesRef = useRef<Particle[]>([]);
    const mouseRef = useRef({ x: -1000, y: -1000 });

    // Keep ref in sync & handle splash
    useEffect(() => {
        // Trigger splash when vacuum stops
        if (!isVacuumActive && isVacuumActiveRef.current) {
            const lastMouseX = mouseRef.current.x;
            const lastMouseY = mouseRef.current.y;

            particlesRef.current.forEach((p) => {
                p.radius = p.originalRadius; // Restore radius

                // Calculate direction from last mouse position
                const dx = p.x - lastMouseX;
                const dy = p.y - lastMouseY;
                const dist = Math.sqrt(dx * dx + dy * dy);

                // Apply an outward force
                const explosionForce = 10 + Math.random() * 10; // Random force magnitude

                // If very close to center, explosion is stronger and random direction
                if (dist < 50) {
                    const angle = Math.random() * Math.PI * 2;
                    p.vx += Math.cos(angle) * (explosionForce * 1.5);
                    p.vy += Math.sin(angle) * (explosionForce * 1.5);
                } else {
                    p.vx += (dx / dist) * explosionForce;
                    p.vy += (dy / dist) * explosionForce;
                }
            });
        }
        isVacuumActiveRef.current = isVacuumActive;
    }, [isVacuumActive]);

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        let width = window.innerWidth;
        let height = window.innerHeight;
        canvas.width = width;
        canvas.height = height;

        // Physics parameters
        const PARTICLE_COUNT = 300;
        const CURSOR_RADIUS = 150;
        const MAX_VELOCITY = 15;

        // Initialize particles randomly if empty
        if (particlesRef.current.length === 0) {
            for (let i = 0; i < PARTICLE_COUNT; i++) {
                particlesRef.current.push(
                    new ParticleImpl(
                        Math.random() * width,
                        Math.random() * height,
                        ctx,
                        width,
                        height,
                        mouseRef,
                        isVacuumActiveRef,
                        CURSOR_RADIUS,
                        MAX_VELOCITY
                    )
                );
            }
        }

        const animate = () => {
            ctx.clearRect(0, 0, width, height);
            particlesRef.current.forEach((p) => {
                p.update();
                p.draw();
            });
            requestAnimationFrame(animate);
        };

        const handleResize = () => {
            width = window.innerWidth;
            height = window.innerHeight;
            canvas.width = width;
            canvas.height = height;
        };

        const handleMouseMove = (e: MouseEvent) => {
            mouseRef.current.x = e.clientX;
            mouseRef.current.y = e.clientY;
        };

        const handleTouchMove = (e: TouchEvent) => {
            if (e.touches.length > 0) {
                mouseRef.current.x = e.touches[0].clientX;
                mouseRef.current.y = e.touches[0].clientY;
            }
        }

        window.addEventListener('resize', handleResize);
        window.addEventListener('mousemove', handleMouseMove);
        window.addEventListener('touchmove', handleTouchMove);

        animate();

        return () => {
            window.removeEventListener('resize', handleResize);
            window.removeEventListener('mousemove', handleMouseMove);
            window.removeEventListener('touchmove', handleTouchMove);
        };
    }, []);

    return (
        <canvas
            ref={canvasRef}
            className="fixed top-0 left-0 w-full h-full pointer-events-none z-50 mix-blend-multiply opacity-60"
        />
    );
};
export default CursorGravity;
