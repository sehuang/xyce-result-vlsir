from __future__ import annotations

import csv
from abc import ABC
from typing import Mapping, Any, Union
        
        
class ResultFile(ABC):
    def __init__(self, file: str) -> None:
        self.file = file
    
    def accept(self, visitor: FileVisitor) -> Mapping[Any, Any]:
        pass


class CSVFile(ResultFile):
    def __init__(self, file: str) -> None:
        super().__init__(file)
        
    def accept(self, visitor: FileVisitor) -> Mapping[Any, Any]:
        return visitor.visit_csv(self)
    

class PRNFile(ResultFile):
    def __init__(self, file: str) -> None:
        super().__init__(file)
        
    def accept(self, visitor: FileVisitor) -> Mapping[Any, Any]:
        return visitor.visit_prn(self)
    
    
class FileVisitor:
    def visit_csv(self, component: ResultFile) -> Mapping[Any, Any]:
        # Parse a CSV output file
        with open(component.file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            vectors = reader.__next__()
            results = dict(zip(vectors, [[]] * len(vectors)))
            idx = enumerate(vectors)
            for row in reader:
                for index in idx:
                    results[index[1]].append(float(row[index[0]]))
        return results
            
    def visit_prn(self, component: ResultFile) -> Mapping[Any, Any]:
        # Parse default text-based output file
        with open(component.file, 'r') as prnfile:
            lines = prnfile.readlines()
            vectors = lines[0].split()
            results = dict(zip(vectors, [[]] * len(vectors)))
            idx = enumerate(vectors)
            for row in lines:
                for index in idx:
                    results[index[1]].append(float(row[index[0]]))
            # If .PRINT given FORMAT=NOINDEX option, there will not be an index 
            # column. If this column is present, drop it as it is redundant
            if "Index" in vectors: results.pop("Index")
            return results
        
    def visit_csd(self, component: ResultFile) -> Mapping[Any, Any]:
        # Parse SPICE Probe file
        with open(component.file, 'r') as csdfile:
            lines = csdfile.readlines()
            # CSD Files appear to have metadata after a "#H" line, then probe 
            # names after "#N", then data points with each time step on a 
            # separate line starting with "#C"
            vector_start_idx = lines.index("#N") + 1
            data_start_idx = lines.index("#C")
            # vectors = " ".join(lines[vector_start_idx:data_start_idx]).split()
            vectors = lines[vector_start_idx:data_start_idx]
            results = dict(zip(['Time'] + vectors, [[]] * len(vectors)))
            index = enumerate(vectors)
            # CSD Files also appear to end with a "#;" ending line, trim this
            for line in lines[data_start_idx:-1]:
                if "#C" in line:
                    # If it's a time line
                    results['Time'].append(line.split()[1])
                else:
                    # Every data point is given as <data>:<column #>, trim off 
                    # the column numbers
                    points = [float(x.split(":")[0]) for x in line.split()]
                    for idx in index:
                        results[idx[1]].append(points(idx[0]))
            return results