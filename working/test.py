def solution(k, score):
    answer = []
    data = []
    for i in score:
        if len(data) <k: 
            
            data.append(i)
            data.sort()
            answer.append(data[0])
            
        else: 
            if data[0] > i: 
                data.sort()
                answer.append(data[0])
                continue
            else: 
                data.pop(0)
                data.append(i)
                data.sort()
                
                answer.append(data[0])
                
                
        
    
    return answer


solution(3,[10, 100, 20, 150, 1, 100, 200])