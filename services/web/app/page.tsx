interface CaseSummary {
  id: string;
  title: string;
  summary: string;
  severity: number;
}

async function getCases(): Promise<CaseSummary[]> {
  try {
    const res = await fetch('http://api:8000/api/v1/cases', {
      cache: 'no-store'
    });

    if (!res.ok) {
      throw new Error(`Failed to fetch cases: ${res.status} ${res.statusText}`);
    }

    return res.json();
  } catch (error) {
    console.error('Error fetching cases:', error);
    return [];
  }
}

export default async function HomePage() {
  const cases = await getCases();

  return (
    <main style={{ fontFamily: 'sans-serif', maxWidth: '800px', margin: '0 auto', padding: '2rem' }}>
      <header style={{ borderBottom: '1px solid #eee', paddingBottom: '1rem', marginBottom: '2rem' }}>
        <h1 style={{ fontSize: '3rem' }}>Parazit.sk</h1>
        <p style={{ color: '#666' }}>Platforma pre transparentné Slovensko</p>
      </header>

      <section>
        <h2 style={{ fontSize: '2rem', marginBottom: '1.5rem' }}>Prehľad monitorovaných káuz</h2>

        {cases.length > 0 ? (
          <div style={{ display: 'grid', gap: '1.5rem' }}>
            {cases.map((caseItem) => (
              <article key={caseItem.id} style={{ border: '1px solid #ddd', padding: '1.5rem', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.05)' }}>
                <h3 style={{ marginTop: 0, fontSize: '1.75rem' }}>{caseItem.title}</h3>
                <p style={{ color: '#333', lineHeight: '1.6' }}>{caseItem.summary}</p>
                <p style={{ fontWeight: 'bold', textAlign: 'right', color: '#444' }}>Závažnosť: {caseItem.severity} / 5</p>
              </article>
            ))}
          </div>
        ) : (
          <p>Nepodarilo sa načítať dáta o kauzách alebo žiadne kauzy neboli nájdené. Skontrolujte, či je backend API spustené a či existujú dátové súbory.</p>
        )}
      </section>
    </main>
  );
}