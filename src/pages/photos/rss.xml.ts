import photos from '../../data/photos.json';

export async function GET() {
  // Sort photos by date (newest first)
  const sortedPhotos = photos.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());

  // Get the most recent photo date for lastBuildDate
  const lastBuildDate = sortedPhotos.length > 0 ? new Date(sortedPhotos[0].date) : new Date();

  // Generate RSS XML
  const rssXml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:media="http://search.yahoo.com/mrss/">
  <channel>
    <title>Ozan's Photography</title>
    <description>Capturing real moments with my Nikon D3300. Street photography, nature, and friends.</description>
    <link>https://ozankaygusuz.pages.dev/photography</link>
    <language>en-us</language>
    <lastBuildDate>${lastBuildDate.toUTCString()}</lastBuildDate>
    <generator>Astro RSS Generator</generator>
    <atom:link href="https://ozankaygusuz.pages.dev/photos/rss.xml" rel="self" type="application/rss+xml"/>
    <image>
      <url>https://ozankaygusuz.pages.dev/images/ozan.png</url>
      <title>Ozan's Photography</title>
      <link>https://ozankaygusuz.pages.dev/photography</link>
    </image>
    ${sortedPhotos.map(photo => {
      const photoUrl = `https://ozankaygusuz.pages.dev${photo.image}`;
      const imageUrl = `https://ozankaygusuz.pages.dev${photo.image}`;
      const pubDate = new Date(photo.date).toUTCString();
      
      return `
    <item>
      <title><![CDATA[${photo.title}]]></title>
      <description><![CDATA[${photo.description}]]></description>
      <link>${photoUrl}</link>
      <guid isPermaLink="true">${photoUrl}</guid>
      <pubDate>${pubDate}</pubDate>
      <category>${photo.category}</category>
      <media:content url="${imageUrl}" type="image/jpeg" medium="image">
        <media:title><![CDATA[${photo.title}]]></media:title>
        <media:description><![CDATA[${photo.description}]]></media:description>
      </media:content>
      <media:thumbnail url="${imageUrl}" width="300" height="300"/>
    </item>`;
    }).join('')}
  </channel>
</rss>`;

  return new Response(rssXml, {
    headers: {
      'Content-Type': 'application/xml',
    },
  });
}

