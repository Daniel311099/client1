import { useEffect, useState } from 'react';

type Data<T> = {
  testData: T;
  fetchFunction: () => Promise<T>;
  isTestMode: boolean;
};

export const useFetchData = <T,>({ testData, fetchFunction, isTestMode }: Data<T>) => {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<Error | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    if (isTestMode) {
      setData(testData);
      setLoading(false);
    } else {
      fetchFunction()
        .then(response => {
          setData(response);
          setLoading(false);
        })
        .catch(err => {
          setError(err);
          setLoading(false);
        });
    }
  }, [isTestMode, testData, fetchFunction]);

  return { data, error, loading };
};