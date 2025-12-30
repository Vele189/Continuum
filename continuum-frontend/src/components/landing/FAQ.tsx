import { useState } from 'react';
import { ChevronDown, ChevronUp } from 'lucide-react';

const FAQ = () => {
    const [openIndex, setOpenIndex] = useState<number | null>(null);

    const toggleFAQ = (index: number) => {
        setOpenIndex(openIndex === index ? null : index);
    };

    const faqs = [
        {
            question: "What is Continuum?",
            answer: "Continuum is an operating system for modern software teams that bridges agile sprint planning with precise time tracking and automated client invoicing."
        },
        {
            question: "How does automatic invoicing work?",
            answer: "Continuum syncs your completed sprint data and tasks to your ledger, automatically populating invoices with every billable hour, saving you manual effort."
        },
        {
            question: "Can I invite clients to the portal?",
            answer: "Yes, the Client Portal gives your clients direct access to real-time project updates, invoice history, and deliverables, fostering transparency."
        },
        {
            question: "Is there a free trial?",
            answer: "Yes, you can start for free to explore the features. We offer scalable plans as your team grows."
        },
        {
            question: "How does time tracking integrate with sprints?",
            answer: "Time tracking is built directly into the sprint board. Developers log time against tasks as they work, ensuring every minute is accounted for in the final invoice."
        }
    ];

    return (
        <section id="faq" className="relative flex flex-col items-center w-full mb-24">
            {/* Text Section */}
            <div
                style={{
                    width: '832px',
                    height: '104px',
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    justifyContent: 'center',
                    gap: '16px',
                    opacity: 1,
                    marginBottom: '48px' // Spacing between header and list
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
                    Frequently asked questions
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
                    Everything you need to know about Continuum.
                </p>
            </div>

            {/* Dropdown Section */}
            <div
                style={{
                    width: '600px',
                    borderRadius: '24px',
                    border: '1px solid #EBEDEE',
                    opacity: 1,
                    overflow: 'hidden', // Ensures content respects border radius
                    background: '#FFFFFF' // Assuming white background for the card
                }}
            >
                {faqs.map((faq, index) => (
                    <div
                        key={index}
                        className="border-b border-[#EBEDEE] last:border-b-0"
                    >
                        <button
                            onClick={() => toggleFAQ(index)}
                            className="w-full flex items-center justify-between p-6 text-left transition-colors hover:bg-gray-50 bg-white"
                            style={{
                                background: '#FFFFFF' // Explicit background
                            }}
                        >
                            <span style={{
                                fontFamily: 'Satoshi',
                                fontWeight: 500,
                                fontSize: '16px',
                                color: '#0B191F'
                            }}>
                                {faq.question}
                            </span>
                            {openIndex === index ? (
                                <ChevronUp className="w-5 h-5 text-[#606D76]" />
                            ) : (
                                <ChevronDown className="w-5 h-5 text-[#606D76]" />
                            )}
                        </button>

                        <div
                            style={{
                                maxHeight: openIndex === index ? '200px' : '0px',
                                opacity: openIndex === index ? 1 : 0,
                                overflow: 'hidden',
                                transition: 'all 0.3s ease-in-out',
                                background: '#FFFFFF'
                            }}
                        >
                            <p style={{
                                fontFamily: 'Satoshi',
                                fontWeight: 400,
                                fontSize: '14px',
                                lineHeight: '24px',
                                color: '#606D76',
                                padding: '0 24px 24px 24px',
                                margin: 0
                            }}>
                                {faq.answer}
                            </p>
                        </div>
                    </div>
                ))}
            </div>
        </section>
    );
};

export default FAQ;
