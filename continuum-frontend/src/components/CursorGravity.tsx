import { useEffect, useRef } from 'react';

const CursorGravity = () => {
    const canvasRef = useRef<HTMLCanvasElement>(null);

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
        const PARTICLE_COUNT = 300; // Matter.js style often has many small items, but we'll use simple particles for "Google Gravity" feel
        const CURSOR_RADIUS = 150;
        const MAX_VELOCITY = 15;

        // Mouse state
        const mouse = { x: -1000, y: -1000 };

        class Particle {
            x: number;
            y: number;
            vx: number;
            vy: number;
            radius: number;
            color: string;
            originalX: number;
            originalY: number;
            friction: number;
            springFactor: number;

            constructor(x: number, y: number) {
                this.x = x;
                this.y = y;
                this.originalX = x;
                this.originalY = y;
                this.vx = 0;
                this.vy = 0;
                this.radius = Math.random() * 2 + 1;
                // Google Gravity style colors often simple, or we can use brand colors
                const colors = ['#4285F4', '#EA4335', '#FBBC05', '#34A853', '#A0C3FF', '#FF9E9E'];
                this.color = colors[Math.floor(Math.random() * colors.length)];
                this.friction = 0.9 + Math.random() * 0.05;
                this.springFactor = 0.01 + Math.random() * 0.02;
            }

            update() {
                const dx = mouse.x - this.x;
                const dy = mouse.y - this.y;
                const dist = Math.sqrt(dx * dx + dy * dy);

                // Attraction to mouse (anti-gravity / magnetic feel)
                // Or repulsion? The user said "follows my cursor around", but often "anti-gravity" implies falling/floating. 
                // "Google Gravity" usually means everything falls down. "Anti-gravity" usually means floating.
                // User said: "follows my cursor around" -> ATTRACTOR.

                if (dist < CURSOR_RADIUS) {
                    // Calculate force for attraction
                    const force = (CURSOR_RADIUS - dist) / CURSOR_RADIUS;
                    const angle = Math.atan2(dy, dx);
                    const fx = Math.cos(angle) * force * 2; // Strength
                    const fy = Math.sin(angle) * force * 2;

                    this.vx += fx;
                    this.vy += fy;
                }

                // Return to original position (elasticity) gives it structure, 
                // OR we can let them flow freely. 
                // Let's make them flow freely but with some drag to not explode.

                // Simulating "space" drag
                this.vx *= 0.95;
                this.vy *= 0.95;

                // Clamp velocity
                const speed = Math.sqrt(this.vx * this.vx + this.vy * this.vy);
                if (speed > MAX_VELOCITY) {
                    const ratio = MAX_VELOCITY / speed;
                    this.vx *= ratio;
                    this.vy *= ratio;
                }

                this.x += this.vx;
                this.y += this.vy;

                // Bounce off walls
                if (this.x < 0 || this.x > width) this.vx *= -1;
                if (this.y < 0 || this.y > height) this.vy *= -1;
            }

            draw() {
                if (!ctx) return;
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
                ctx.fillStyle = this.color;
                ctx.fill();
                ctx.closePath();
            }
        }

        // Initialize particles randomly
        const particles: Particle[] = [];
        for (let i = 0; i < PARTICLE_COUNT; i++) {
            particles.push(new Particle(Math.random() * width, Math.random() * height));
        }

        const animate = () => {
            ctx.clearRect(0, 0, width, height);
            particles.forEach(p => {
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
            mouse.x = e.clientX;
            mouse.y = e.clientY;
        };

        // For touch devices
        const handleTouchMove = (e: TouchEvent) => {
            if (e.touches.length > 0) {
                mouse.x = e.touches[0].clientX;
                mouse.y = e.touches[0].clientY;
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
