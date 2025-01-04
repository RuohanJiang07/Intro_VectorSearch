import React, { useState } from 'react';
import { Search, Loader2, ArrowUpRight } from 'lucide-react';
import { 
  Card, 
  CardHeader,
  CardTitle, 
  CardDescription, 
  CardContent 
} from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';

const VectorSearchPortal = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [searchMode, setSearchMode] = useState('vector'); // Default to 'vector'

  const handleSearch = async () => {
    if (!query.trim()) return;
    
    setIsLoading(true);
    try {
      const endpoint = searchMode === 'vector' 
        ? 'http://localhost:8000/api/search' 
        : 'http://localhost:8000/api/traditional_search';
      
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: query }),
      });
      
      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error('Search failed:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <Card className="mb-8">
        <CardHeader>
          <CardTitle className="text-2xl font-bold">Expert Search Portal</CardTitle>
          <CardDescription>
            Search through our database of experts using natural language (Vector Search) or exact keywords (Traditional Search).
          </CardDescription>
        </CardHeader>
        <CardContent>
          {/* Search Mode Selector */}
          <div className="flex gap-4 mb-4 items-center">
            <div className="w-48">
              <label htmlFor="searchMode" className="block text-sm font-medium text-gray-700">
                Search Mode
              </label>
              <select
                id="searchMode"
                value={searchMode}
                onChange={(e) => setSearchMode(e.target.value)}
                className="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              >
                <option value="vector">Vector Search</option>
                <option value="traditional">Traditional Search</option>
              </select>
            </div>

            {/* Search Input */}
            <Input
              type="text"
              placeholder="Enter your search query..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="flex-1"
              onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
            />
            <Button 
              onClick={handleSearch}
              disabled={isLoading}
              className="min-w-24"
              variant="primary"
            >
              {isLoading ? (
                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
              ) : (
                <Search className="w-4 h-4 mr-2" />
              )}
              Search
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Results Section */}
      {results.length > 0 && (
        <div className="space-y-4">
          {results.map((result, index) => (
            <Card key={index}>
              <CardContent className="pt-6">
                <div className="flex justify-between items-start mb-2">
                  <div className="flex-grow">
                    <h3 className="text-lg font-semibold">{result.Name}</h3>
                    <p className="text-sm text-gray-500">
                      {result.Category} • {result.Label}
                    </p>
                  </div>
                  <div className="flex items-center gap-4">
                    {result.Similarity !== undefined && (
                      <span className="text-sm bg-blue-100 text-blue-800 px-2 py-1 rounded">
                        {(result.Similarity * 100).toFixed(1)}% Match
                      </span>
                    )}
                    {result.url && (
                      <a 
                        href={result.url} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="p-2 hover:bg-gray-100 rounded-full transition-colors"
                      >
                        <ArrowUpRight className="w-5 h-5 text-gray-600 hover:text-blue-600" />
                      </a>
                    )}
                  </div>
                </div>
                <p className="text-gray-700 mt-2">{result.Explanation || result.Profile_Chunk}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* No Results State */}
      {results.length === 0 && query && !isLoading && (
        <Card>
          <CardContent className="p-6 text-center text-gray-500">
            No results found for your search query.
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default VectorSearchPortal;
