
import { useState, useEffect, useRef } from 'react';

const Hero = () => {
  const [activeSection, setActiveSection] = useState(0);
  const [isHeroHovered, setIsHeroHovered] = useState(false);
  const [isInvoiceHovered, setIsInvoiceHovered] = useState(false);
  const sectionRefs = [useRef<HTMLDivElement>(null), useRef<HTMLDivElement>(null), useRef<HTMLDivElement>(null)];

  useEffect(() => {
    const observers = sectionRefs.map((ref, index) => {
      if (!ref.current) return null;

      const observer = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              setActiveSection(index);
            }
          });
        },
        {
          threshold: [0, 0.1],
          rootMargin: '-45% 0px -45% 0px'
        }
      );

      observer.observe(ref.current);
      return observer;
    });

    return () => {
      observers.forEach((observer) => {
        if (observer) {
          observer.disconnect();
        }
      });
    };
  }, []);
  return (
    <section className="relative flex flex-col items-center w-full" style={{ paddingTop: '190px' }}>
      <div style={{ width: '776px', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '24px' }}>

        {/* Main Heading */}
        <h1 className="flex flex-col items-center justify-center text-center">
          <div className="flex items-center justify-center flex-wrap gap-3" style={{ lineHeight: '104%' }}>
            <span style={{
              display: 'inline-block',
              fontFamily: 'Sarina',
              fontWeight: 400,
              fontSize: '62px',
              lineHeight: '1.5',
              background: 'linear-gradient(99.31deg, #24B5F8 4.62%, #5521FE 148.53%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              backgroundClip: 'text',
              color: 'transparent',
              padding: '0 5px 15px 5px', // Top/Bottom padding for glyphs
              marginBottom: '-15px' // Compensate for extra bottom padding to align with "connects"
            }}>
              Continuum
            </span>
            <span style={{
              fontFamily: 'Satoshi',
              fontWeight: 500,
              fontSize: '62px',
              color: '#000000',
              paddingBottom: '10px'
            }}>
              connects
            </span>
          </div>
          <span style={{
            fontFamily: 'Satoshi',
            fontWeight: 500,
            fontSize: '62px',
            color: '#000000',
            lineHeight: '104%'
          }}>
            delivery with profitability.
          </span>
        </h1>

        {/* Subheading */}
        <p style={{
          fontFamily: 'Satoshi',
          fontWeight: 500,
          fontSize: '16px',
          lineHeight: '100%',
          textAlign: 'center',
          color: '#606D76',
          maxWidth: '600px'
        }}>
          The operating system for modern software teams. Seamlessly bridge the gap
          between agile sprint planning, precise time tracking, and client invoicing.
        </p>

        {/* Start for free Button */}
        <button
          className="flex items-center justify-center transition-all duration-200 hover:scale-105"
          style={{
            width: '115px',
            height: '32px',
            background: '#FFFFFF',
            border: '1px solid #EDEDED',
            borderRadius: '8px',
            padding: '8px 16px',
            gap: '8px'
          }}
          onMouseEnter={() => setIsHeroHovered(true)}
          onMouseLeave={() => setIsHeroHovered(false)}
        >
          <span style={{
            fontFamily: 'Satoshi',
            fontWeight: 700,
            fontSize: '14px',
            lineHeight: '100%',
            letterSpacing: '0%',
            color: '#0B191F',
            whiteSpace: 'nowrap'
          }}>
            Start for free
          </span>
        </button>
      </div>

      {/* Feature Images */}
      {/* Container needs overflow-visible to allow large images to be seen fully */}
      <div className="relative w-full mt-16 flex justify-center items-start perspective-[1000px] overflow-visible pointer-events-none mb-0">
        {/* Middle Image - Main */}
        <div
          className="relative z-30 pointer-events-auto transition-transform duration-500 ease-[cubic-bezier(0.25,1,0.5,1)]"
          style={{
            transform: isHeroHovered ? 'scale(1.05)' : 'scale(1)'
          }}
        >
          <img
            src="/landing-page/middle-image.png"
            alt="Dashboard Main"
            style={{
              width: '1566px',
              height: '1010px',
              objectFit: 'contain',
              maxWidth: 'none' // Ensure it doesn't shrink
            }}
          />
        </div>

        {/* Left Image */}
        <img
          src="/landing-page/left-image.png"
          alt="Dashboard Left"
          className="absolute top-[30px] z-10 opacity-100 transition-all duration-700 ease-[cubic-bezier(0.25,1,0.5,1)]"
          style={{
            width: '846px',
            height: '808px',
            objectFit: 'contain',
            maxWidth: 'none',
            left: '50%',
            transform: isHeroHovered
              ? 'translateX(-50%) rotate(0deg) scale(0.9)'
              : 'translateX(-110%) rotate(-6deg)',
            transformOrigin: 'bottom right'
          }}
        />

        {/* Right Image */}
        <img
          src="/landing-page/right-image.png"
          alt="Dashboard Right"
          className="absolute top-[30px] z-20 opacity-100 transition-all duration-700 ease-[cubic-bezier(0.25,1,0.5,1)]"
          style={{
            width: '846px',
            height: '808px',
            objectFit: 'contain',
            maxWidth: 'none',
            left: '50%',
            transform: isHeroHovered
              ? 'translateX(-50%) rotate(0deg) scale(0.9)'
              : 'translateX(10%) rotate(6deg)',
            transformOrigin: 'bottom left'
          }}
        />
      </div>

      {/* Designed for Deep Work Section */}
      <div id="deep-work" className="relative flex flex-col items-center justify-center gap-4 -mt-[20px] pointer-events-auto" style={{
        width: '776px',
        opacity: 1,
        zIndex: 40 // Ensure it's above other elements if needed
      }}>
        {/* Heading */}
        <h2 style={{
          fontFamily: 'Satoshi',
          fontWeight: 500,
          fontStyle: 'normal',
          fontSize: '62px',
          lineHeight: '104%',
          letterSpacing: '0%',
          textAlign: 'center',
          color: '#0B191F'
        }}>
          Designed for deep work
        </h2>

        {/* Subheading */}
        <p style={{
          fontFamily: 'Satoshi',
          fontWeight: 500,
          fontStyle: 'normal',
          fontSize: '16px',
          lineHeight: '24px',
          letterSpacing: '0%',
          textAlign: 'center',
          color: '#606D76'
        }}>
          Eliminate administrative drag. Continuum gets out of the way so your team can<br />
          focus on shipping.
        </p>
      </div>

      {/* Feature Cards Grid */}
      <div
        className="relative mx-auto mt-12 mb-20"
        style={{
          width: '1187px',
          gap: '12px',
          opacity: 1,
          display: 'flex',
          flexDirection: 'column'
        }}
      >
        {/* Top Row */}
        <div
          style={{
            display: 'flex',
            gap: '12px',
            marginBottom: '12px'
          }}
        >
          {/* Top Left Card */}
          <div
            className="group"
            style={{
              width: '700px',
              height: '564px',
              borderRadius: '36px',
              opacity: 1,
              overflow: 'hidden'
            }}
          >
            <img
              src="/landing-page/top-left.png"
              alt="Frictionless Time Logging"
              className="transition-transform duration-500 ease-out group-hover:scale-105"
              style={{
                width: '100%',
                height: '100%',
                objectFit: 'cover',
                display: 'block'
              }}
            />
          </div>

          {/* Top Right Card */}
          <div
            className="group"
            style={{
              width: '473px',
              height: '564px',
              borderRadius: '36px',
              opacity: 1,
              overflow: 'hidden'
            }}
          >
            <img
              src="/landing-page/top-right.png"
              alt="Integrated Invoicing"
              className="transition-transform duration-500 ease-out group-hover:scale-105"
              style={{
                width: '100%',
                height: '100%',
                objectFit: 'cover',
                display: 'block'
              }}
            />
          </div>
        </div>

        {/* Bottom Card */}
        <div
          className="group"
          style={{
            width: '1187px',
            height: '306px',
            borderRadius: '36px',
            opacity: 1,
            overflow: 'hidden'
          }}
        >
          <img
            src="/landing-page/bottom.png"
            alt="Real-time Project Health"
            className="transition-transform duration-500 ease-out group-hover:scale-105"
            style={{
              width: '100%',
              height: '100%',
              objectFit: 'cover',
              display: 'block'
            }}
          />
        </div>
      </div>

      {/* Master your methodology Section */}
      <div
        id="methodology"
        className="relative mx-auto mt-12 mb-12"
        style={{
          width: '1161px',
          height: '128px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          opacity: 1
        }}
      >
        <h2 style={{
          fontFamily: 'Satoshi',
          fontWeight: 500,
          fontStyle: 'normal',
          fontSize: '62px',
          lineHeight: '104%',
          letterSpacing: '0%',
          color: '#0B191F',
          margin: 0
        }}>
          Master your<br />methodology.
        </h2>
      </div>

      {/* Feature Sections */}
      <div
        className="relative mx-auto mb-20"
        style={{
          width: '1161px',
          display: 'flex',
          gap: '36px',
          opacity: 1
        }}
      >
        {/* Sprint Cycles Section */}
        <div
          style={{
            width: '349px',
            height: '218px',
            opacity: 1,
            display: 'flex',
            flexDirection: 'column',
            gap: '16px'
          }}
        >
          {/* Icon */}
          <img
            src="/icons/notebook-pen.svg"
            alt="Sprint Cycles"
            style={{
              width: '40px',
              height: '40px',
              transform: 'translateZ(0)',
              willChange: 'transform'
            }}
          />

          {/* Heading */}
          <h3 style={{
            fontFamily: 'Satoshi',
            fontWeight: 500,
            fontStyle: 'normal',
            fontSize: '38.32px',
            lineHeight: '104%',
            letterSpacing: '0%',
            color: '#0B191F',
            margin: 0
          }}>
            Sprint Cycles
          </h3>

          {/* Description */}
          <p style={{
            fontFamily: 'Satoshi',
            fontWeight: 500,
            fontStyle: 'normal',
            fontSize: '16px',
            lineHeight: '26px',
            letterSpacing: '0%',
            color: '#606D76',
            margin: 0
          }}>
            Plan, execute, and review. Move work from the backlog into active sprints and track progress toward the finish line.
          </p>
        </div>

        {/* Flexible Views Section */}
        <div
          style={{
            width: '349px',
            height: '218px',
            opacity: 1,
            display: 'flex',
            flexDirection: 'column',
            gap: '16px'
          }}
        >
          {/* Icons */}
          <div
            style={{
              display: 'flex',
              gap: '8px',
              alignItems: 'center'
            }}
          >
            {/* Board Icon - Highlighted */}
            <div
              style={{
                width: '94px',
                height: '40px',
                borderRadius: '8px',
                padding: '8px 16px',
                background: 'linear-gradient(180deg, #CFECFF 0%, #CFECFF 100%)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px',
                transform: 'translateZ(0)',
                willChange: 'transform'
              }}
            >
              <img src="/icons/square-kanban.svg" alt="Board" style={{ width: '16px', height: '16px' }} />
              <span style={{
                fontFamily: 'Satoshi',
                fontWeight: 500,
                fontSize: '14px',
                lineHeight: '100%',
                letterSpacing: '0%',
                color: '#043E59'
              }}>
                Board
              </span>
            </div>

            {/* List Icon */}
            <div
              style={{
                width: '40px',
                height: '40px',
                borderRadius: '8px',
                padding: '8px 12px',
                background: '#EDF0F3',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px',
                transform: 'translateZ(0)',
                willChange: 'transform'
              }}
            >
              <img src="/icons/list.svg" alt="List" style={{ width: '16px', height: '16px' }} />
            </div>

            {/* Grid Icon */}
            <div
              style={{
                width: '40px',
                height: '40px',
                borderRadius: '8px',
                padding: '8px 12px',
                background: '#EDF0F3',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px',
                transform: 'translateZ(0)',
                willChange: 'transform'
              }}
            >
              <img src="/icons/square-chart-gantt.svg" alt="Gantt" style={{ width: '16px', height: '16px' }} />
            </div>

            {/* Calendar Icon */}
            <div
              style={{
                width: '40px',
                height: '40px',
                borderRadius: '8px',
                padding: '8px 12px',
                background: '#EDF0F3',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px',
                transform: 'translateZ(0)',
                willChange: 'transform'
              }}
            >
              <img src="/icons/calendar.svg" alt="Calendar" style={{ width: '16px', height: '16px' }} />
            </div>
          </div>

          {/* Heading */}
          <h3 style={{
            fontFamily: 'Satoshi',
            fontWeight: 500,
            fontStyle: 'normal',
            fontSize: '38.32px',
            lineHeight: '104%',
            letterSpacing: '0%',
            color: '#0B191F',
            margin: 0
          }}>
            Flexible Views
          </h3>

          {/* Description */}
          <p style={{
            fontFamily: 'Satoshi',
            fontWeight: 500,
            fontStyle: 'normal',
            fontSize: '16px',
            lineHeight: '26px',
            letterSpacing: '0%',
            color: '#606D76',
            margin: 0
          }}>
            Visualize work your way. Toggle instantly between Kanban boards for flow, lists for density, and calendars for deadlines.
          </p>
        </div>

        {/* Full ownership Section */}
        <div
          style={{
            width: '349px',
            height: '218px',
            opacity: 1,
            display: 'flex',
            flexDirection: 'column',
            gap: '16px'
          }}
        >
          {/* Icons */}
          <div
            style={{
              display: 'flex',
              gap: '8px',
              alignItems: 'center'
            }}
          >
            {/* Owner Icon - Highlighted */}
            <div
              style={{
                width: '94px',
                height: '40px',
                borderRadius: '8px',
                padding: '8px 16px',
                background: 'linear-gradient(180deg, #CFECFF 0%, #CFECFF 100%)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px',
                transform: 'translateZ(0)',
                willChange: 'transform'
              }}
            >
              <img src="/icons/square-user.svg" alt="Owner" style={{ width: '16px', height: '16px' }} />
              <span style={{
                fontFamily: 'Satoshi',
                fontWeight: 500,
                fontSize: '14px',
                lineHeight: '100%',
                letterSpacing: '0%',
                color: '#043E59'
              }}>
                Owner
              </span>
            </div>

            {/* Document Icon 1 */}
            <div
              style={{
                width: '40px',
                height: '40px',
                borderRadius: '8px',
                padding: '8px 12px',
                background: '#EDF0F3',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px',
                transform: 'translateZ(0)',
                willChange: 'transform'
              }}
            >
              <img src="/icons/square-user.svg" alt="User 1" style={{ width: '16px', height: '16px' }} />
            </div>

            {/* Document Icon 2 */}
            <div
              style={{
                width: '40px',
                height: '40px',
                borderRadius: '8px',
                padding: '8px 12px',
                background: '#EDF0F3',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px',
                transform: 'translateZ(0)',
                willChange: 'transform'
              }}
            >
              <img src="/icons/square-user.svg" alt="User 2" style={{ width: '16px', height: '16px' }} />
            </div>
          </div>

          {/* Heading */}
          <h3 style={{
            fontFamily: 'Satoshi',
            fontWeight: 500,
            fontStyle: 'normal',
            fontSize: '38.32px',
            lineHeight: '104%',
            letterSpacing: '0%',
            color: '#0B191F',
            margin: 0
          }}>
            Full ownership
          </h3>

          {/* Description */}
          <p style={{
            fontFamily: 'Satoshi',
            fontWeight: 500,
            fontStyle: 'normal',
            fontSize: '16px',
            lineHeight: '26px',
            letterSpacing: '0%',
            color: '#606D76',
            margin: 0
          }}>
            The only role with the power to build sprints, invite members, set billing rates, and finalize client invoices.
          </p>
        </div>
      </div>

      {/* Automatic monthly invoicing Section */}
      <div
        id="invoicing"
        className="relative mx-auto mt-12 mb-12"
        style={{
          width: '832px',
          height: '104px',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          gap: '16px',
          opacity: 1
        }}
      >
        <h2 style={{
          fontFamily: 'Satoshi',
          fontWeight: 500,
          fontStyle: 'normal',
          fontSize: '62px',
          lineHeight: '104%',
          letterSpacing: '0%',
          textAlign: 'center',
          color: '#0B191F',
          margin: 0
        }}>
          Automatic monthly invoicing
        </h2>
      </div>

      {/* Invoice and Features Section */}
      <div
        className="relative mx-auto mb-20"
        style={{
          display: 'flex',
          gap: '68px',
          alignItems: 'flex-start',
          justifyContent: 'center',
          opacity: 1,
          maxWidth: '1400px',
          padding: '0 20px'
        }}
      >
        {/* Invoice Image with Shadow */}
        <div
          style={{
            position: 'relative',
            width: '600px',
            height: '808.33px',
            flexShrink: 0
          }}
        >
          {/* Second Shadow Div - Behind the first shadow */}
          <div
            style={{
              position: 'absolute',
              width: '600px',
              height: '783px',
              top: '52px',
              left: '-50px',
              borderRadius: '36px',
              border: '1px solid #EBEDEE',
              background: '#FFFFFF',
              opacity: isInvoiceHovered ? 0 : 1,
              zIndex: 1,
              transition: 'opacity 0.5s ease-in-out'
            }}
          />

          {/* Shadow Div - Behind the image */}
          <div
            style={{
              position: 'absolute',
              width: '600px',
              height: '785px',
              top: '26px',
              left: '-25px',
              borderRadius: '36px',
              border: '1px solid #EBEDEE',
              background: '#FFFFFF',
              opacity: isInvoiceHovered ? 0 : 1,
              zIndex: 2,
              transition: 'opacity 0.5s ease-in-out'
            }}
          />

          {/* Invoice Image - On top */}
          <div
            onMouseEnter={() => setIsInvoiceHovered(true)}
            onMouseLeave={() => setIsInvoiceHovered(false)}
            style={{
              position: 'relative',
              width: '100%',
              height: '100%',
              zIndex: 3,
              transform: isInvoiceHovered ? 'translate(-50px, 52px)' : 'translate(0, 0)',
              transition: 'transform 0.5s ease-in-out'
            }}
          >
            <img
              src="/landing-page/invoice.png"
              alt="Invoice Interface"
              style={{
                width: '100%',
                height: '100%',
                objectFit: 'contain',
                display: 'block'
              }}
            />
          </div>
        </div>

        {/* Text Sections - Aligned with invoice height */}
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between',
            height: '808.33px',
            flex: 1,
            maxWidth: '500px'
          }}
        >
          {/* Section 1: Sync sprints to your ledger */}
          <div
            ref={sectionRefs[0]}
            style={{
              display: 'flex',
              gap: '16px',
              alignItems: 'flex-start'
            }}
          >
            {/* Blue Vertical Line - Only show if active */}
            {activeSection === 0 ? (
              <div
                style={{
                  width: '4px',
                  height: '182px',
                  backgroundColor: '#2E99F9',
                  opacity: 1,
                  flexShrink: 0,
                  transition: 'opacity 0.8s ease-in-out',
                  borderRadius: '4px'
                }}
              />
            ) : (
              <div
                style={{
                  width: '4px',
                  height: '182px',
                  backgroundColor: '#2E99F9',
                  opacity: 0,
                  flexShrink: 0,
                  transition: 'opacity 0.8s ease-in-out',
                  borderRadius: '4px'
                }}
              />
            )}

            {/* Text Content */}
            <div
              style={{
                display: 'flex',
                flexDirection: 'column',
                gap: '12px',
                maxWidth: '400px'
              }}
            >
              <h3 style={{
                fontFamily: 'Satoshi',
                fontWeight: 500,
                fontStyle: 'normal',
                fontSize: '38.32px',
                lineHeight: '104%',
                letterSpacing: '0%',
                color: activeSection === 0 ? '#0B191F' : '#606D76',
                margin: 0,
                transition: 'color 0.8s ease-in-out'
              }}>
                Sync sprints to your ledger
              </h3>
              <p style={{
                fontFamily: 'Satoshi',
                fontWeight: 500,
                fontStyle: 'normal',
                fontSize: '16px',
                lineHeight: '26px',
                letterSpacing: '0%',
                color: '#606D76',
                margin: 0
              }}>
                Auto-populate invoices with completed sprint data and tasks, capturing every billable hour without the manual effort.
              </p>
            </div>
          </div>

          {/* Section 2: Precision billing by project */}
          <div
            ref={sectionRefs[1]}
            style={{
              display: 'flex',
              gap: '16px',
              alignItems: 'flex-start'
            }}
          >
            {/* Blue Vertical Line - Only show if active */}
            {activeSection === 1 ? (
              <div
                style={{
                  width: '4px',
                  height: '182px',
                  backgroundColor: '#2E99F9',
                  opacity: 1,
                  flexShrink: 0,
                  transition: 'opacity 0.8s ease-in-out',
                  borderRadius: '4px'
                }}
              />
            ) : (
              <div
                style={{
                  width: '4px',
                  height: '182px',
                  backgroundColor: '#2E99F9',
                  opacity: 0,
                  flexShrink: 0,
                  transition: 'opacity 0.8s ease-in-out',
                  borderRadius: '4px'
                }}
              />
            )}

            {/* Text Content */}
            <div
              style={{
                display: 'flex',
                flexDirection: 'column',
                gap: '12px',
                maxWidth: '400px'
              }}
            >
              <h3 style={{
                fontFamily: 'Satoshi',
                fontWeight: 500,
                fontStyle: 'normal',
                fontSize: '38.32px',
                lineHeight: '104%',
                letterSpacing: '0%',
                color: activeSection === 1 ? '#0B191F' : '#606D76',
                margin: 0,
                transition: 'color 0.8s ease-in-out'
              }}>
                Precision billing by project
              </h3>
              <p style={{
                fontFamily: 'Satoshi',
                fontWeight: 500,
                fontStyle: 'normal',
                fontSize: '16px',
                lineHeight: '26px',
                letterSpacing: '0%',
                color: '#606D76',
                margin: 0
              }}>
                Set your rates once and let Continuum calculate totals and taxes for instant, accurate billing in one click.
              </p>
            </div>
          </div>

          {/* Section 3: From review to PDF */}
          <div
            ref={sectionRefs[2]}
            style={{
              display: 'flex',
              gap: '16px',
              alignItems: 'flex-start'
            }}
          >
            {/* Blue Vertical Line - Only show if active */}
            {activeSection === 2 ? (
              <div
                style={{
                  width: '4px',
                  height: '182px',
                  backgroundColor: '#2E99F9',
                  opacity: 1,
                  flexShrink: 0,
                  transition: 'opacity 0.8s ease-in-out',
                  borderRadius: '4px'
                }}
              />
            ) : (
              <div
                style={{
                  width: '4px',
                  height: '182px',
                  backgroundColor: '#2E99F9',
                  opacity: 0,
                  flexShrink: 0,
                  transition: 'opacity 0.8s ease-in-out',
                  borderRadius: '4px'
                }}
              />
            )}

            {/* Text Content */}
            <div
              style={{
                display: 'flex',
                flexDirection: 'column',
                gap: '12px',
                maxWidth: '400px'
              }}
            >
              <h3 style={{
                fontFamily: 'Satoshi',
                fontWeight: 500,
                fontStyle: 'normal',
                fontSize: '38.32px',
                lineHeight: '104%',
                letterSpacing: '0%',
                color: activeSection === 2 ? '#0B191F' : '#606D76',
                margin: 0,
                transition: 'color 0.8s ease-in-out'
              }}>
                From review to PDF
              </h3>
              <p style={{
                fontFamily: 'Satoshi',
                fontWeight: 500,
                fontStyle: 'normal',
                fontSize: '16px',
                lineHeight: '26px',
                letterSpacing: '0%',
                color: '#606D76',
                margin: 0
              }}>
                Finalise auto-generated drafts instantly. One click updates your records and delivers a professional breakdown to your client.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Client Portal Section */}
      <div
        id="clients"
        className="relative mx-auto mt-12 mb-20"
        style={{
          width: '832px',
          height: '104px',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          gap: '16px',
          opacity: 1
        }}
      >
        <h2 style={{
          fontFamily: 'Satoshi',
          fontWeight: 500,
          fontStyle: 'normal',
          fontSize: '62px',
          lineHeight: '104%',
          letterSpacing: '0%',
          textAlign: 'center',
          color: '#0B191F',
          margin: 0
        }}>
          Client Portal
        </h2>
        <p style={{
          fontFamily: 'Satoshi',
          fontWeight: 500,
          fontStyle: 'normal',
          fontSize: '16px',
          lineHeight: '24px',
          letterSpacing: '0%',
          textAlign: 'center',
          color: '#606D76',
          margin: 0
        }}>
          Coming soon. Give your clients direct access to project updates, invoices, and deliverables in real-time.
        </p>
      </div>

      {/* Client Portal Background Container */}
      <div
        className="relative mx-auto mb-20"
        style={{
          width: '1187px',
          height: '955.75px',
          borderRadius: '36px',
          padding: '48px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'flex-start',
          opacity: 1,
          backgroundColor: '#FFFFFF',
          backgroundImage: 'linear-gradient(180deg, rgba(178, 247, 194, 0.48) 0%, rgba(253, 251, 247, 0.48) 100%)',
          boxShadow: `
            0px 2px 3px 0px rgba(181, 181, 181, 0.24),
            0px 6px 6px 0px rgba(181, 181, 181, 0.20),
            0px 14px 8px 0px rgba(181, 181, 181, 0.12),
            0px 25px 10px 0px rgba(181, 181, 181, 0.04),
            0px 39px 11px 0px rgba(181, 181, 181, 0.00)
          `
        }}
      >
        {/* Left Section */}
        <div
          style={{
            width: '332px',
            height: '859.75px',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between',
            opacity: 1,
            alignSelf: 'flex-start',
            position: 'relative',
            flexShrink: 0
          }}
        >
          {/* Top Content */}
          <div
            style={{
              display: 'flex',
              flexDirection: 'column',
              margin: 0,
              padding: 0
            }}
          >
            {/* Heading */}
            <h2 style={{
              fontFamily: 'Satoshi',
              fontWeight: 500,
              fontStyle: 'normal',
              fontSize: '38.32px',
              lineHeight: '104%',
              letterSpacing: '0%',
              color: '#0B191F',
              margin: 0,
              marginBottom: '24px',
              padding: 0,
              display: 'block'
            }}>
              Real-time Project Health
            </h2>

            {/* Description */}
            <p style={{
              fontFamily: 'Satoshi',
              fontWeight: 500,
              fontStyle: 'normal',
              fontSize: '16px',
              lineHeight: '26px',
              letterSpacing: '0%',
              color: '#606D76',
              margin: 0,
              marginBottom: '36px'
            }}>
              Never be surprised by a missed deadline. Track velocity and see instantly if a project is 'Project On Track' or 'At Risk.'
            </p>

            {/* Start for free Button */}
            <button
              style={{
                width: '115px',
                height: '32px',
                borderRadius: '8px',
                border: '1px solid #EDEDED',
                padding: '8px 16px',
                gap: '8px',
                opacity: 1,
                background: '#FFFFFF',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                cursor: 'pointer',
                boxShadow: `
                  0px 1px 1px 0px rgba(14, 34, 34, 0.03),
                  0px 2px 1px 0px rgba(14, 34, 34, 0.02),
                  0px 3px 1px 0px rgba(14, 34, 34, 0.01),
                  0px 5px 1px 0px rgba(14, 34, 34, 0.00)
                `
              }}
            >
              <span style={{
                fontFamily: 'Satoshi',
                fontWeight: 700,
                fontStyle: 'normal',
                fontSize: '14px',
                lineHeight: '100%',
                letterSpacing: '0%',
                color: '#0B191F',
                whiteSpace: 'nowrap'
              }}>
                Start for free
              </span>
            </button>
          </div>

          {/* Bottom Disclaimer */}
          <p style={{
            fontFamily: 'Satoshi',
            fontWeight: 500,
            fontStyle: 'normal',
            fontSize: '14px',
            lineHeight: '20px',
            letterSpacing: '0%',
            color: '#606D76',
            margin: 0
          }}>
            Disclaimer goes here
          </p>
        </div>

        {/* Right Section - Dashboard Image */}
        <div
          style={{
            width: '900px',
            height: '1050px',
            flexShrink: 0,
            alignSelf: 'flex-start',
            margin: 0,
            marginTop: '-100px',
            marginRight: '-60px',
            padding: 0,
            position: 'relative',
            top: 0
          }}
        >
          <img
            src="/landing-page/client-portal-components/background.png"
            alt="Client Portal Dashboard"
            style={{
              width: '100%',
              height: '100%',
              objectFit: 'contain',
              display: 'block',
              margin: 0,
              padding: 0,
              verticalAlign: 'top',
              lineHeight: 0
            }}
          />
        </div>
      </div>
    </section>
  );
};

export default Hero;
