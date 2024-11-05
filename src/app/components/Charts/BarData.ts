interface testBarChart {
    name: string;
    total: number;
    predicted: number;
  }
  
  export type DataSets = {
    [key: string]: testBarChart[];
  }
  
  export function getBarChart(): DataSets {
    return {
      Classe_1: [
        { name: 'Jan', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'Feb', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'Mar', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'Apr', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'May', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'Jun', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'Jul', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
      ],
      Classe_2: [
        { name: 'Jan', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'Feb', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'Mar', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'Apr', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'May', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'Jun', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'Jul', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
      ],
      Classe_3: [
        { name: 'Jan', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'Feb', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'Mar', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'Apr', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'May', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'Jun', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'Jul', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
      ],
      Classe_4: [
        { name: 'Jan', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'Feb', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'Mar', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'Apr', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'May', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'Jun', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'Jul', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
      ],
      Classe_5: [
        { name: 'Jan', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'Feb', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'Mar', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'Apr', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'May', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'Jun', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'Jul', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
      ],
      Classe_6: [
        { name: 'Jan', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'Feb', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'Mar', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'Apr', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'May', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'Jun', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'Jul', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
      ],
      Classe_7: [
        { name: 'Jan', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'Feb', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'Mar', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'Apr', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'May', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'Jun', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'Jul', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
      ],
      Classe_8: [
        { name: 'Jan', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'Feb', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'Mar', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'Apr', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'May', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'Jun', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'Jul', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
      ],
      Classe_9: [
        { name: 'Jan', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'Feb', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'Mar', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'Apr', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'May', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'Jun', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
        { name: 'Jul', total: Math.floor(Math.random() * 3000) + 1000, predicted: Math.floor(Math.random() * 3000) + 1000 },
      ],
    };
  }
  